from datetime import time, timedelta, datetime

from utils.constants import PLANNER_SCHEDULE
from utils.models_orm import Slot, Event


class Day:
    def __init__(self, slots: list[Slot], schedule: dict = PLANNER_SCHEDULE):
        self._schedule = schedule
        self.create_daily_schedule(slots)

    @staticmethod
    def _check_slots(slots: list[Slot]):
        dates = set()
        for slot in slots:
            dates.add(slot.start_date)
            if len(dates) > 1:
                # logger.error()
                raise ValueError('Slots contain more than one date')

    def _delete_used_slot(self, slot: Slot):
        dt = datetime.combine(datetime.today(), slot.start_time)
        time_end = (dt + timedelta(minutes=slot.event.duration)).time()
        for time_from_schedule in self._schedule.copy():
            if slot.start_time < time_from_schedule < time_end:
                self._schedule.pop(time_from_schedule)

    def create_daily_schedule(self, slots: list[Slot]) -> None:
        for slot in slots:
            self._delete_used_slot(slot)
            self._schedule[slot.start_time] = slot

    @property
    def schedule(self):
        return self._schedule

class Week(Day):
    pass


class Year(Week):
    pass

d = Day(
    [
        Slot(start_time=time(10), event=Event(duration=90)),
        Slot(start_time=time(14, 30), event=Event(duration=120))
    ]
)
pprint(d.schedule)
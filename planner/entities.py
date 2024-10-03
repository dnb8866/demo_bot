from datetime import time, timedelta, datetime

from utils.constants import PLANNER_DAY_SCHEDULE, PLANNER_WEEK_SCHEDULE
from utils.models_orm import Slot, Event


class Day:
    def __init__(
            self,
            slots: list[Slot] = None,
            schedule: dict = PLANNER_DAY_SCHEDULE
    ):
        self.schedule = schedule.copy()
        self.date = None
        self.create_daily_schedule(slots) if slots else None

    @staticmethod
    def _check_slots(slots: list[Slot]) -> bool:
        dates = set()
        for slot in slots:
            dates.add(slot.start_date)
            if len(dates) > 1:
                # logger.error()
                return False
        return True

    def _delete_used_slot(self, slot: Slot) -> None:
        dt = datetime.combine(datetime.today(), slot.start_time)
        time_end = (dt + timedelta(minutes=slot.event.duration)).time()
        for time_from_schedule in self.schedule.copy():
            if slot.start_time < time_from_schedule < time_end:
                self.schedule.pop(time_from_schedule)

    def create_daily_schedule(self, slots: list[Slot]) -> None:
        if not self._check_slots(slots):
            # logger.error()
            raise ValueError('Список слотов содержит более 1 даты.')
        self.date = slots[0].start_date
        for slot in slots:
            self._delete_used_slot(slot)
            self.schedule[slot.start_time] = slot

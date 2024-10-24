from datetime import time

import pytest

from planner.entities import Day


class TestPlanner:

    def test_day_schedule(self, slots):
        day = Day(slots[:-1])
        assert day.schedule == {
            time(9, 0): None,
            time(9, 30): None,
            time(10, 0): slots[0],
            time(11, 30): None,
            time(12, 0): None,
            time(12, 30): None,
            time(13, 0): slots[1],
            time(15, 0): None,
            time(15, 30): None,
            time(16, 0): None,
            time(16, 30): None,
            time(17, 0): slots[2]
        }
        day = Day(slots[:-2])
        assert day.schedule == {
            time(9, 0): None,
            time(9, 30): None,
            time(10, 0): slots[0],
            time(11, 30): None,
            time(12, 0): None,
            time(12, 30): None,
            time(13, 0): slots[1],
            time(15, 0): None,
            time(15, 30): None,
            time(16, 0): None,
            time(16, 30): None,
            time(17, 0): None,
            time(17, 30): None
        }

    def test_check_many_dates(self, slots):
        with pytest.raises(ValueError, match='Список слотов содержит более 1 даты.'):
            Day(slots)

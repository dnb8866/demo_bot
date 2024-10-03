from datetime import time

import config as cfg
from utils.assist import frange

PLANNER_DAY_SCHEDULE = {
    time(hour=int(time_value), minute=int((time_value - int(time_value)) * 60)): None
    for time_value in frange(cfg.START_WORK_DAY_HOUR,
                             cfg.END_WORK_DAY_HOUR,
                             1 / (60 / cfg.MIN_SLOT_DURATION_MINUTES))
}

PLANNER_WEEK_SCHEDULE = {
    key: None
    for key in range(1, 8)
}

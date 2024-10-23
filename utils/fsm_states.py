from aiogram.fsm.state import StatesGroup, State


class PaymentFsm(StatesGroup):
    pay = State()


class ShopFsm(StatesGroup):
    item_info = State()
    test = State()


class PlannerFsm(StatesGroup):
    edit_available_dates = State()
    get_dates = State()
    get_date_for_show = State()

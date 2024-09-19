from aiogram.fsm.state import StatesGroup, State


class PaymentFsm(StatesGroup):
    pay = State()


class ShopFsm(StatesGroup):
    item_info = State()
    test = State()

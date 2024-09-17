from aiogram.fsm.state import StatesGroup, State


class ShopFsm(StatesGroup):
    item_info = State()
    test = State()

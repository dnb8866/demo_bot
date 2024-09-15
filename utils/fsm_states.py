from aiogram.fsm.state import StatesGroup, State


class ShopFsm(StatesGroup):
    buy_now = State()

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

import utils.texts as t
from config import SBER_TOKEN, YOOKASSA_TOKEN, PAYMASTER_TOKEN
from engine import telegram_bot as bot, shop_repo
from utils.fsm_states import PaymentFsm
from utils.keyboards import PaymentKB, KB

router = Router()


@router.callback_query(F.data == 'planner')
async def payment(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(await t.planner_welcome(), reply_markup=PaymentKB.payment())

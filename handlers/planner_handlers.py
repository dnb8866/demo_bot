from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

import utils.texts as t
from config import SBER_TOKEN, YOOKASSA_TOKEN, PAYMASTER_TOKEN
from engine import telegram_bot as bot, shop_repo
from utils.fsm_states import PaymentFsm
from utils.keyboards import KB, PlannerKB

router = Router()


@router.callback_query(F.data == 'planner')
async def payment(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(await t.planner_welcome(), reply_markup=PlannerKB.main())


@router.callback_query(F.data == 'planner_for_admin')
async def admin(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(await t.planner_welcome(), reply_markup=KB.back_to_main())


@router.callback_query(F.data == 'available_dates')
async def available_dates(callback: types.CallbackQuery, state: FSMContext):
    pass


@router.callback_query(F.data == 'planner_for_client')
async def client(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(await t.planner_welcome(), reply_markup=KB.back_to_main())

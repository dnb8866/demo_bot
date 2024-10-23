from datetime import datetime

from aiogram import Router, types, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext

import utils.texts as t
from engine import planner_repo, telegram_bot
from utils import assist
from utils.fsm_states import PlannerFsm
from utils.keyboards import PlannerKB
from utils import validators

router = Router()


@router.callback_query(F.data == 'planner')
async def payment(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(await t.planner_welcome(), reply_markup=PlannerKB.main())


@router.callback_query(F.data == 'planner_for_admin')
async def admin(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(await t.planner_welcome(), reply_markup=PlannerKB.main_admin())


@router.callback_query(F.data == 'edit_available_dates')
async def edit_available_dates(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(PlannerFsm.edit_available_dates)
    dt = datetime.now()
    current_month_dates = await planner_repo.get_all_available_dates(dt.month, dt.year)
    next_month_dates = await planner_repo.get_all_available_dates(
        dt.month + 1 if dt.month < 12 else 1,
        dt.year if dt.month < 12 else dt.year + 1
    )
    # await callback.message.edit_text(
    #     await t.planner_available_dates(current_month_dates, next_month_dates),
    #     reply_markup=PlannerKB.edit_available_dates()
    # )

    # DEMO TEXT
    next_month_number = dt.month + 1 if dt.month < 12 else 1
    year = dt.year if dt.month < 12 else dt.year + 1
    text = (f'Открытые даты для записи в текущем месяце ({t.MONTH_TEXT[dt.month]} {dt.year}):\n'
            f'2, 3, 4, 5, 6, 11, 12, 13, 14, 15, 18, 19, 20, 21, 22, 23, 25, 26, 27\n\n'
            f'Открытые даты для записи в следующем месяце ({t.MONTH_TEXT[next_month_number]} {year}):\n'
            f'2, 3, 4, 5, 6, 11, 12, 13, 14, 15, 18, 19, 20, 26, 27')
    await callback.message.edit_text(
        text,
        reply_markup=PlannerKB.edit_available_dates()
    )


@router.callback_query(F.data == 'add_available_dates', PlannerFsm.edit_available_dates)
async def add_available_dates(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(type_data='add')
    await callback.message.edit_text(await t.planner_choose_month(), reply_markup=PlannerKB.choose_month())


@router.callback_query(F.data == 'remove_available_dates', PlannerFsm.edit_available_dates)
async def remove_available_dates(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(type_data='remove')
    await callback.message.edit_text(await t.planner_choose_month(), reply_markup=PlannerKB.choose_month())


@router.callback_query(PlannerFsm.edit_available_dates)
async def set_month(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'p_current_month':
        await state.update_data(month=datetime.now().month, year=datetime.now().year)
    elif callback.data == 'p_next_month':
        await state.update_data(month=datetime.now().month+1, year=datetime.now().year+1)
    await state.set_state(PlannerFsm.get_dates)
    msg = await callback.message.edit_text(
        await t.planner_get_dates((await state.get_data())['type_data']),
        reply_markup=PlannerKB.back_to_planner()
    )
    await state.update_data(prev_msg_id=msg.message_id)


@router.message(PlannerFsm.get_dates)
async def set_dates(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await assist.delete_prev_messages(telegram_bot, message, data['prev_msg_id'])
    if await validators.validate_dates(message.text, data['month'], data['year']):
        msg = await message.answer(
            await t.success_change_dates(data['type_data']),
            reply_markup=PlannerKB.back_to_planner()
        )
    else:
        try:
            msg = await message.answer(
                await t.invalid_dates(data['type_data']),
                reply_markup=PlannerKB.back_to_planner()
            )
        except TelegramBadRequest:
            msg = await telegram_bot.answer()
    await state.update_data(prev_msg_id=msg.message_id)


@router.callback_query(F.data == 'show_slots')
async def show_slots(callback: types.CallbackQuery, state: FSMContext):
    dt = datetime.now()
    next_month_number = dt.month + 1 if dt.month < 12 else 1
    year = dt.year if dt.month < 12 else dt.year + 1
    await state.set_state(PlannerFsm.get_date_for_show)
    await callback.message.edit_text(
        'Даты, в которых есть записи\n\n'
        f'{t.MONTH_TEXT[dt.month]} {dt.year}:\n'
        f'6, 11, 12, 13, 14, 15, 18, 19, 20, 21, 22\n\n'
        f'{t.MONTH_TEXT[next_month_number]} {year}:\n'
        f'2, 3, 4, 5, 6, 11, 12, 13, 14, 15, 18, 19, 20\n\n'
        f'Введите дату в формате ДД.ММ.ГГГ, чтобы посмотреть записи данного дня'
    )


@router.message(PlannerFsm.get_date_for_show)
async def show_slots_for_date(message: types.Message, state: FSMContext):
    pass


@router.callback_query(F.data == 'planner_for_client')
async def client(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(await t.planner_welcome(), reply_markup=PlannerKB.main_client())

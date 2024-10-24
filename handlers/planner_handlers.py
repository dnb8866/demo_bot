from datetime import datetime, time, date

from aiogram import Router, types, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext

import utils.texts as t
from engine import planner_repo, telegram_bot
from planner.entities import Day
from utils import assist
from utils.fsm_states import PlannerFsm
from utils.keyboards import PlannerKB
from utils import validators
from utils.models_orm import Slot, SlotDate, Event, User
from utils.validators import validate_date

router = Router()


@router.callback_query(F.data == 'planner')
async def payment(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(await t.planner_welcome(), reply_markup=PlannerKB.main())


@router.callback_query(F.data == 'planner_for_admin')
async def admin(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
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
        reply_markup=PlannerKB.edit_available_dates_for_admin()
    )


@router.callback_query(F.data == 'add_available_dates', PlannerFsm.edit_available_dates)
async def add_available_dates(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(type_data='add')
    await callback.message.edit_text(await t.planner_choose_month(), reply_markup=PlannerKB.choose_month_for_admin())


@router.callback_query(F.data == 'remove_available_dates', PlannerFsm.edit_available_dates)
async def remove_available_dates(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(type_data='remove')
    await callback.message.edit_text(await t.planner_choose_month(), reply_markup=PlannerKB.choose_month_for_admin())


@router.callback_query(PlannerFsm.edit_available_dates)
async def set_month(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'p_current_month':
        await state.update_data(month=datetime.now().month, year=datetime.now().year)
    elif callback.data == 'p_next_month':
        await state.update_data(month=datetime.now().month+1, year=datetime.now().year+1)
    await state.set_state(PlannerFsm.get_dates)
    msg = await callback.message.edit_text(
        await t.planner_get_dates((await state.get_data())['type_data']),
        reply_markup=PlannerKB.back_to_planner_for_admin()
    )
    await state.update_data(prev_msg_id=msg.message_id)


@router.message(PlannerFsm.get_dates)
async def set_dates(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await assist.delete_prev_messages(telegram_bot, message, data['prev_msg_id'])
    if await validators.validate_dates(message.text, data['month'], data['year']):
        msg = await message.answer(
            await t.success_change_dates(data['type_data']),
            reply_markup=PlannerKB.back_to_planner_for_admin()
        )
    else:
        try:
            msg = await message.answer(
                await t.invalid_dates(data['type_data']),
                reply_markup=PlannerKB.back_to_planner_for_admin()
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
    msg = await callback.message.edit_text(
        'ДЕМО\n\n'
        'Даты, в которых есть записи\n\n'
        f'{t.MONTH_TEXT[dt.month]} {dt.year}:\n'
        f'6, 13, 22\n\n'
        f'{t.MONTH_TEXT[next_month_number]} {year}:\n'
        f'2, 18\n\n'
        f'{await t.show_slots()}',
        reply_markup=PlannerKB.back_to_planner_for_admin()
    )
    await state.update_data(prev_msg_id=msg.message_id)


@router.message(PlannerFsm.get_date_for_show)
async def show_slots_for_date(message: types.Message, state: FSMContext):
    # DEMO пример
    user_1 = User(firstname='Сергей', lastname='Петров', phone_number=79001112233)
    user_2 = User(firstname='Петр', lastname='Сергеев', phone_number=79003332211)
    user_3 = User(firstname='Ольга', lastname='Попова', phone_number=79007778899)
    event_1 = Event(name='Прием', duration=90)
    event_2 = Event(name='Консультация', duration=120)
    event_3 = Event(name='Повторный прием', duration=45)
    slot_1 = Slot(event=event_1, slot_date=SlotDate(slot_date=date(2024, 1, 1)), start_time=time(10), user=user_1)
    slot_2 = Slot(event=event_2, slot_date=SlotDate(slot_date=date(2024, 1, 1)), start_time=time(13), user=user_2)
    slot_3 = Slot(event=event_3, slot_date=SlotDate(slot_date=date(2024, 1, 1)), start_time=time(17), user=user_3)
    day = Day(slots=(slot_1, slot_2, slot_3))
    data = await state.get_data()
    await assist.delete_prev_messages(telegram_bot, message, data['prev_msg_id'])
    dt = datetime.now()
    next_month = dt.month + 1 if dt.month < 12 else 1
    year = dt.year if dt.month < 12 else dt.year + 1
    dates = (
        date(dt.year, dt.month, 6),
        date(dt.year, dt.month, 13),
        date(dt.year, dt.month, 22),
        date(year, next_month, 2),
        date(year, next_month, 18)
    )
    if cleaned_date := await validate_date(message.text):
        if cleaned_date in dates:
            msg = await message.answer(
                f'ДЕМО\n\n'
                f'{await t.planner_show_date(cleaned_date.strftime("%d.%m.%Y"), day)}',
                reply_markup=PlannerKB.show_slots()
            )
        else:
            msg = await message.answer(
                f'На {cleaned_date.strftime("%d.%m.%Y")} отсутствуют записи.',
                reply_markup=PlannerKB.show_slots()
            )
    else:
        try:
            msg = await message.answer(
                await t.invalid_date(),
                reply_markup=PlannerKB.show_slots()
            )
        except TelegramBadRequest:
            msg = await telegram_bot.answer()
    await state.update_data(prev_msg_id=msg.message_id)



@router.callback_query(F.data == 'accept_slots')
async def accept_slots(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        'Просмотр, подтверждение и отмена записей через веб интерфейс. Недоступно в демо режиме.',
        reply_markup=PlannerKB.back_to_planner_for_admin()
    )


@router.callback_query(F.data == 'reject_slots')
async def accept_slots(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        'Просмотр, подтверждение и отмена записей через веб интерфейс. Недоступно в демо режиме.',
        reply_markup=PlannerKB.back_to_planner_for_admin()
    )


@router.callback_query(F.data == 'planner_for_client')
async def client(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(await t.planner_welcome(), reply_markup=PlannerKB.main_client())


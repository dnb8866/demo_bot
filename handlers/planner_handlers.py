from datetime import datetime

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

import utils.texts as t
from engine import planner_repo
from utils.fsm_states import PlannerFsm
from utils.keyboards import PlannerKB

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
    await callback.message.edit_text(
        await t.planner_available_dates(current_month_dates, next_month_dates),
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
        await state.update_data(month='current')
    elif callback.data == 'p_next_month':
        await state.update_data(month='next')
    await state.set_state(PlannerFsm.get_dates)
    await callback.message.edit_text(
        await t.planner_get_dates((await state.get_data())['type_data']),
        reply_markup=PlannerKB.back_to_planner()
    )

@router.callback_query(PlannerFsm.get_dates)
async def set_dates(callback: types.CallbackQuery, state: FSMContext):
    pass


@router.callback_query(F.data == 'show_slots')
async def show_slots(callback: types.CallbackQuery, state: FSMContext):
    pass


@router.callback_query(F.data == 'planner_for_client')
async def client(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(await t.planner_welcome(), reply_markup=PlannerKB.main_client())

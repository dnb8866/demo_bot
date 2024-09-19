from datetime import datetime

from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

import utils.texts as t
from engine import shop_repo, user_repo
from utils.keyboards import KB
from utils.models_orm import User

router = Router()


@router.message(Command('start'))
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    user = await user_repo.get(message.from_user.id)
    if not user:
        dt_now = datetime.utcnow()
        user = User(
            id=message.from_user.id,
            firstname=message.from_user.first_name,
            lastname=message.from_user.last_name,
            username=message.from_user.username,
            created=dt_now,
            updated=dt_now,
        )
        await user_repo.add(user)
    await message.answer(await t.main(message.from_user.first_name),
                         reply_markup=KB.main())


@router.callback_query(F.data == 'start')
async def start_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(await t.main(callback.from_user.first_name),
                                     reply_markup=KB.main())


@router.callback_query(F.data == 'remove_notice')
async def remove_notice(callback: types.CallbackQuery):
    await callback.message.delete()

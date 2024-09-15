from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

import utils.texts as t
from utils.keyboards import PaymentKB
from utils.services import Robokassa, Yookassa

router = Router()


@router.callback_query(F.data == 'payment')
async def payment(callback: types.CallbackQuery):
    link = Robokassa().generate_payment_link('test_dnb8866', 'cH7tLk79OWP92sWchFrf', cost=500, number=1, description='Тест', is_test=1)
    await callback.message.edit_text(t.payment_description(), reply_markup=PaymentKB.payment(link))


@router.callback_query(F.data == 'payment_robokassa')
async def payment_robokassa(callback: types.CallbackQuery):
    link = Robokassa().generate_payment_link('test_dnb8866', 'cH7tLk79OWP92sWchFrf', cost=500, number=1, description='Тест', is_test=1)
    await callback.message.edit_text(link, reply_markup=PaymentKB.back_to_payment())


@router.callback_query(F.data == 'payment_yookassa')
async def payment_yookassa(callback: types.CallbackQuery):
    res = await Yookassa.create()
    print(res)
    await callback.message.edit_text('123', reply_markup=PaymentKB.back_to_payment())


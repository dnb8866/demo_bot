from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

import utils.texts as t
from config import SBER_TOKEN, YOOKASSA_TOKEN, PAYMASTER_TOKEN
from engine import telegram_bot as bot
from utils.fsm_states import PaymentFsm
from utils.keyboards import PaymentKB, KB

router = Router()


@router.callback_query(F.data == 'payment')
async def payment(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(PaymentFsm.pay)
    msg = await callback.message.edit_text(await t.payment_description(), reply_markup=PaymentKB.payment())
    await state.update_data(msg=msg.message_id)


@router.callback_query(F.data == 'payment_sber', PaymentFsm.pay)
async def payment_sber(callback: types.CallbackQuery):
    price = types.LabeledPrice(label='Тест1', amount=12345)
    if SBER_TOKEN.split(':')[1] == 'TEST':
        await bot.send_invoice(
            callback.message.chat.id,
            title='title',
            description='description',
            provider_token=SBER_TOKEN,
            currency='rub',
            is_flexible=False,
            prices=[price],
            start_parameter='time-machine-example',
            payload='test_order_123'
        )


@router.callback_query(F.data == 'payment_yookassa', PaymentFsm.pay)
async def payment_sber(callback: types.CallbackQuery):
    price = types.LabeledPrice(label='Тест2', amount=23456)
    if YOOKASSA_TOKEN.split(':')[1] == 'TEST':
        await bot.send_invoice(
            callback.message.chat.id,
            title='title',
            description='description',
            provider_token=YOOKASSA_TOKEN,
            currency='rub',
            is_flexible=False,  # True если конечная цена зависит от способа доставки
            prices=[price],
            start_parameter='time-machine-example',
            payload='test_order_123'
        )


@router.callback_query(F.data == 'payment_paymaster', PaymentFsm.pay)
async def payment_sber(callback: types.CallbackQuery):
    price = types.LabeledPrice(label='Тест3', amount=34567)
    if YOOKASSA_TOKEN.split(':')[1] == 'TEST':
        await bot.send_invoice(
            callback.message.chat.id,
            title='title',
            description='description',
            provider_token=PAYMASTER_TOKEN,
            currency='rub',
            is_flexible=False,  # True если конечная цена зависит от способа доставки
            prices=[price],
            start_parameter='time-machine-example',
            payload='test_order_123'
        )


@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@router.message(F.successful_payment)
async def process_successful_payment(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await bot.delete_message(message.chat.id, data['msg'])
    await message.answer('Платеж успешно проведен.', reply_markup=KB.back_to_main())
    # pmnt = message.successful_payment
    # print(pmnt)

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

import utils.texts as t
from engine import shop_repo
from utils.fsm_states import ShopFsm
from utils.keyboards import ShopKB

router = Router()


@router.callback_query(F.data == 'shop')
async def shop(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    categories = await shop_repo.get_categories()
    await callback.message.edit_text(
        t.shop(), reply_markup=ShopKB.choose(categories, 'category')
    )


@router.callback_query(F.data.startswith('category_'))
async def category(callback: types.CallbackQuery, state: FSMContext):
    items = await shop_repo.get_items_by_category(int(callback.data.split('_')[1]))
    await callback.message.edit_text(
        t.items(), reply_markup=ShopKB.choose(items, 'item', back_to_shop_button=True)
    )


@router.callback_query(F.data.startswith('item_'))
async def item(callback: types.CallbackQuery, state: FSMContext):
    item_obj = await shop_repo.get_item(int(callback.data.split('_')[1]))
    amount = 1
    await state.set_state(ShopFsm.item_info)
    await state.update_data(
        item_id=item_obj.id,
        item_name=item_obj.name,
        item_price=item_obj.price,
        item_description=item_obj.description,
        amount=amount
    )
    await callback.message.edit_text(
        t.item(item_obj.name, item_obj.description, item_obj.price, amount),
        reply_markup=ShopKB.item()
    )


@router.callback_query(F.data.startswith('change_amount_'), ShopFsm.item_info)
async def change_amount(callback: types.CallbackQuery, state: FSMContext):
    change_number = int(callback.data.split('_')[2])
    data = await state.get_data()
    amount = data.get('amount', 1)
    if change_number < 0 and amount == 1:
        await callback.answer()
        return
    amount += change_number
    await state.update_data(amount=amount)
    await callback.message.edit_text(
        t.item(data.get('item_name'), data.get('item_description'), data.get('item_price'), amount),
        reply_markup=ShopKB.item()
    )


@router.callback_query(F.data == 'add_to_cart', ShopFsm.item_info)
async def add_to_cart(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await shop_repo.add_order_item(callback.from_user.id, data.get('item_id'), data.get('amount'))
    await callback.message.edit_text('Добавлено в корзину', reply_markup=ShopKB.back_to_shop())


@router.callback_query(F.data == 'show_cart')
async def show_cart(callback: types.CallbackQuery, state: FSMContext):
    order_items = await shop_repo.get_all_order_items(callback.from_user.id, without_order=True)
    await callback.message.edit_text(order_items, reply_markup=ShopKB.back_to_shop())

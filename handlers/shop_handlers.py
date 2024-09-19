from decimal import Decimal

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

import utils.assist as assist
import utils.texts as t
from engine import shop_repo
from utils.fsm_states import ShopFsm
from utils.keyboards import ShopKB
from utils.models_orm import Order

router = Router()


@router.callback_query(F.data == 'shop')
async def shop(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    categories = await shop_repo.get_categories()
    await callback.message.edit_text(
        await t.shop(), reply_markup=ShopKB.choose(categories, 'category', my_orders_button=True)
    )


@router.callback_query(F.data.startswith('category_'))
async def category(callback: types.CallbackQuery, state: FSMContext):
    items = await shop_repo.get_items_by_category(int(callback.data.split('_')[1]))
    await callback.message.edit_text(
        await t.items(), reply_markup=ShopKB.choose(items, 'item', back_to_shop_button=True)
    )


@router.callback_query(F.data.startswith('item_'))
async def item(callback: types.CallbackQuery, state: FSMContext):
    item_obj = await shop_repo.get_item(int(callback.data.split('_')[1]))
    quantity = 1
    await state.set_state(ShopFsm.item_info)
    await state.update_data(
        item_id=item_obj.id,
        item_name=item_obj.name,
        item_price=item_obj.price,
        item_description=item_obj.description,
        quantity=quantity
    )
    await callback.message.edit_text(
        await t.item(item_obj.name, item_obj.description, item_obj.price, quantity),
        reply_markup=ShopKB.item()
    )


@router.callback_query(F.data.startswith('change_quantity_'), ShopFsm.item_info)
async def change_quantity(callback: types.CallbackQuery, state: FSMContext):
    change_number = int(callback.data.split('_')[2])
    data = await state.get_data()
    quantity = data.get('quantity', 1)
    if change_number < 0 and quantity == 1:
        await callback.answer()
        return
    quantity += change_number
    await state.update_data(quantity=quantity)
    await callback.message.edit_text(
        await t.item(data.get('item_name'), data.get('item_description'), data.get('item_price'), quantity),
        reply_markup=ShopKB.item()
    )


@router.callback_query(F.data == 'add_to_cart', ShopFsm.item_info)
async def add_to_cart(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await shop_repo.add_order_item(callback.from_user.id, data.get('item_id'), data.get('quantity'))
    await callback.message.edit_text('Добавлено в корзину', reply_markup=ShopKB.back_to_shop())


@router.callback_query(F.data == 'show_cart')
async def show_cart(callback: types.CallbackQuery):
    order_items = await shop_repo.get_all_order_items(callback.from_user.id, without_order=True)
    total_price = await assist.calculate_total_price_from_items(order_items)
    await callback.message.edit_text(await t.show_cart(order_items, total_price), reply_markup=ShopKB.show_cart())


@router.callback_query(F.data == 'clean_cart')
async def clean_cart(callback: types.CallbackQuery):
    order_items = await shop_repo.get_all_order_items(callback.from_user.id, without_order=True)
    try:
        for order_item in order_items:
            await shop_repo.delete_order_item(order_item.id)
    except Exception as _e:
        # logger.error(f"{type(_e)} - {_e}")
        await callback.message.edit_text(f"Ошибка: {type(_e)} - {_e}")
    await callback.message.edit_text('Корзина очищена', reply_markup=ShopKB.back_to_shop())


@router.callback_query(F.data == 'place_order')
async def place_order(callback: types.CallbackQuery):
    order_items = await shop_repo.get_all_order_items(callback.from_user.id, without_order=True)
    # total_price = await assist.calculate_total_price_from_cart(order_items)
    await shop_repo.create_order(callback.from_user.id, order_items)
    await callback.message.edit_text('Заказ оформлен', reply_markup=ShopKB.back_to_shop())


@router.callback_query(F.data == 'my_orders')
async def my_orders(callback: types.CallbackQuery):
    orders = await shop_repo.get_all_orders_from_user(callback.from_user.id)
    await callback.message.edit_text(await t.all_orders_from_user(orders), reply_markup=ShopKB.back_to_shop())

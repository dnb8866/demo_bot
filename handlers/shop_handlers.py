from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

import utils.texts as t
from engine import repo
from utils.fsm_states import ShopFsm
from utils.keyboards import ShopKB

router = Router()


@router.callback_query(F.data == 'shop')
async def shop(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    categories = await repo.get_categories()
    await callback.message.edit_text(
        t.shop(), reply_markup=ShopKB.choose(categories, 'category')
    )


@router.callback_query(F.data.startswith('category_'))
async def category(callback: types.CallbackQuery):
    items = await repo.get_items_by_category(int(callback.data.split('_')[1]))
    await callback.message.edit_text(
        t.items(), reply_markup=ShopKB.choose(items, 'item', back_to_shop_button=True)
    )


@router.callback_query(F.data.startswith('item_'))
async def item(callback: types.CallbackQuery, state: FSMContext):
    item_obj = await repo.get_item(int(callback.data.split('_')[1]))
    await state.set_state(ShopFsm.buy_now)
    await state.update_data(
        item_id=item_obj.id,
        item_name=item_obj.name,
        item_price=item_obj.price,
        item_description=item_obj.description,
    )
    await callback.message.edit_text(t.item(item_obj), reply_markup=ShopKB.item())


@router.callback_query(ShopFsm.buy_now)
async def buy_set_amount(callback: types.CallbackQuery, state: FSMContext):
    change_number = int(callback.data.split('_')[1])
    data = await state.get_data()
    amount = data.get('amount', 1)
    if change_number < 0 and amount == 1:
        await callback.answer()
        return
    amount += change_number
    await state.update_data(amount=amount)
    await callback.message.edit_text(f'{amount}\n\n{data}', reply_markup=ShopKB.set_amount())


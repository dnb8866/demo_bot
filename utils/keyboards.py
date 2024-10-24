from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder


class KB:

    b_shop = InlineKeyboardButton(text='🏪 Магазин', callback_data='shop')
    b_payment = InlineKeyboardButton(text='💳 Оплата', callback_data='payment')
    b_monitoring = InlineKeyboardButton(text='👁 Мониторинг', url='https://t.me/MyCryptoInformer_bot')
    b_planner = InlineKeyboardButton(text='Бронирование времени', callback_data='planner')
    b_finances = InlineKeyboardButton(text='💰 Управление финансами', url='https://t.me/family_finances_app_bot')
    b_parser = InlineKeyboardButton(text='📝 Парсер', url='https://t.me/dnb8866_bot')
    b_questions = InlineKeyboardButton(text='📍 Опрос', callback_data='questions')
    b_moderate = InlineKeyboardButton(text='💻 Модерирование', callback_data='moderate')
    b_admin = InlineKeyboardButton(text='⚙️ Админка', callback_data='admin')

    b_back_to_main = InlineKeyboardButton(text='🔙 На главную', callback_data='start')

    b_remove_notice = InlineKeyboardButton(text='Удалить сообщение', callback_data='remove_notice')

    @classmethod
    def main(cls) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.row(cls.b_shop, cls.b_payment)
        builder.row(cls.b_monitoring, cls.b_parser)
        builder.row(cls.b_planner)
        builder.row(cls.b_finances)
        builder.row(cls.b_questions, cls.b_moderate)
        builder.row(cls.b_admin)
        return builder.as_markup()

    @classmethod
    def back_to_main(cls) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.add(cls.b_back_to_main)
        return builder.as_markup()

    @classmethod
    def remove_notice(cls) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.add(cls.b_remove_notice)
        return builder.as_markup()


class PaymentKB(KB):

    b_payment_sber = InlineKeyboardButton(text='Сбер', callback_data='payment_sber')
    b_payment_yookassa = InlineKeyboardButton(text='ЮКасса', callback_data='payment_yookassa')
    b_payment_paymaster = InlineKeyboardButton(text='PayMaster', callback_data='payment_paymaster')

    b_back_to_payment = InlineKeyboardButton(text='Назад', callback_data='payment')

    @classmethod
    def payment(cls) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.add(
            cls.b_payment_sber,
            cls.b_payment_paymaster,
            cls.b_payment_yookassa,
            cls.b_back_to_main)
        return builder.adjust(1).as_markup()

    @classmethod
    def back_to_payment(cls) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.add(cls.b_back_to_payment)
        return builder.as_markup()


class ShopKB(KB):
    b_buy = InlineKeyboardButton(text='💰 Купить', callback_data='buy')
    b_add_to_cart = InlineKeyboardButton(text='🛒 Добавить в корзину', callback_data='add_to_cart')
    b_show_cart = InlineKeyboardButton(text='🛒 Просмотреть корзину', callback_data='show_cart')
    b_clean_cart = InlineKeyboardButton(text='🧹 Очистить корзину', callback_data='clean_cart')
    b_place_order = InlineKeyboardButton(text='💰 Оплатить заказ', callback_data='place_order')
    b_my_orders = InlineKeyboardButton(text='📋 Мои заказы', callback_data='my_orders')
    b_increace_quantity = InlineKeyboardButton(text='+', callback_data='change_quantity_1')
    b_decreace_quantity = InlineKeyboardButton(text='-', callback_data='change_quantity_-1')

    @classmethod
    def back_to_shop(cls) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.add(cls.b_shop)
        return builder.as_markup()

    @classmethod
    def choose(
            cls,
            categories: list[tuple[int, str]],
            prefix: str,
            back_to_shop_button: bool = False,
            my_orders_button: bool = False
    ) -> InlineKeyboardMarkup:

        builder = InlineKeyboardBuilder()
        for i, (id_, text) in enumerate(categories):
            if i % 2 == 0:
                builder.row(InlineKeyboardButton(text=text, callback_data=f'{prefix}_{id_}'))
            else:
                builder.add(InlineKeyboardButton(text=text, callback_data=f'{prefix}_{id_}'))
        builder.row(cls.b_show_cart)
        if my_orders_button:
            builder.row(cls.b_my_orders)
        if back_to_shop_button:
            builder.row(cls.b_shop)
        builder.row(cls.b_back_to_main)
        return builder.as_markup()

    @classmethod
    def item(cls) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.add(
            cls.b_buy,
            cls.b_add_to_cart,
            cls.b_decreace_quantity, cls.b_increace_quantity,
            cls.b_shop,
            cls.b_back_to_main)
        return builder.adjust(1, 1, 2, 1).as_markup()

    @classmethod
    def show_cart(cls) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.add(cls.b_place_order, cls.b_clean_cart, cls.b_shop)
        return builder.adjust(1).as_markup()


class PlannerKB(KB):

    b_for_admin = InlineKeyboardButton(text='Для владельца', callback_data='planner_for_admin')
    b_edit_available_dates = InlineKeyboardButton(text='Редактировать даты', callback_data='edit_available_dates')
    b_current_month = InlineKeyboardButton(text='В текущий месяц', callback_data='p_current_month')
    b_next_month = InlineKeyboardButton(text='В следующий месяц', callback_data='p_next_month')
    b_add_available_dates = InlineKeyboardButton(text='Добавить даты', callback_data='add_available_dates')
    b_remove_available_dates = InlineKeyboardButton(text='Удалить даты', callback_data='remove_available_dates')
    b_show_slots = InlineKeyboardButton(text='Показать записи', callback_data='show_slots')
    b_accept_slots = InlineKeyboardButton(text='Подтвердить записи', callback_data='accept_slots')
    b_reject_slots = InlineKeyboardButton(text='Отменить записи', callback_data='reject_slots')

    b_for_client = InlineKeyboardButton(text='Для клиента', callback_data='planner_for_client')
    b_add_slot = InlineKeyboardButton(text='Забронировать слот', callback_data='add_slot')
    b_cancel_slot = InlineKeyboardButton(text='Отменить запись', callback_data='cancel_slot')
    b_my_slots = InlineKeyboardButton(text='Мои записи', callback_data='my_slots')

    b_back_to_planner = InlineKeyboardButton(text='Назад', callback_data='planner')
    b_back_to_planner_for_admin = InlineKeyboardButton(text='Назад', callback_data='planner_for_admin')
    b_back_to_planner_for_client = InlineKeyboardButton(text='Назад', callback_data='planner_for_client')

    @classmethod
    def back_to_planner(cls) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.add(cls.b_back_to_planner, cls.b_back_to_main)
        return builder.adjust(1).as_markup()

    @classmethod
    def back_to_planner_for_admin(cls) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.add(cls.b_back_to_planner_for_admin, cls.b_back_to_main)
        return builder.adjust(1).as_markup()

    @classmethod
    def back_to_planner_for_client(cls) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.add(cls.b_back_to_planner_for_client, cls.b_back_to_main)
        return builder.adjust(1).as_markup()

    @classmethod
    def main(cls) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.row(cls.b_for_client, cls.b_for_admin, cls.b_back_to_main)
        return builder.adjust(1).as_markup()

    @classmethod
    def main_admin(cls) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.add(
            cls.b_edit_available_dates,
            cls.b_show_slots,
            cls.b_accept_slots,
            cls.b_reject_slots,
            cls.b_back_to_main
        )
        return builder.adjust(1).as_markup()

    @classmethod
    def main_client(cls) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.add(
            cls.b_add_slot,
            cls.b_cancel_slot,
            cls.b_my_slots,
            cls.b_back_to_main
        )
        return builder.adjust(1).as_markup()

    @classmethod
    def edit_available_dates_for_admin(cls) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.add(
            cls.b_add_available_dates,
            cls.b_remove_available_dates,
            cls.b_back_to_planner_for_admin,
            cls.b_back_to_main
        )
        return builder.adjust(1).as_markup()

    @classmethod
    def choose_month_for_admin(cls) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.add(
            cls.b_current_month,
            cls.b_next_month,
            cls.b_back_to_planner_for_admin,
            cls.b_back_to_main
        )
        return builder.adjust(1).as_markup()

    @classmethod
    def show_slots(cls):
        builder = InlineKeyboardBuilder()
        builder.add(
            cls.b_show_slots,
            cls.b_back_to_planner,
            cls.b_back_to_main
        )
        return builder.adjust(1).as_markup()

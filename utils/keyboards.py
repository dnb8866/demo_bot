from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder


class KB:

    b_shop = InlineKeyboardButton(text='🏪 Магазин', callback_data='shop')
    b_payment = InlineKeyboardButton(text='💳 Оплата', callback_data='payment')
    b_monitoring = InlineKeyboardButton(text='👁 Мониторинг', callback_data='monitoring')
    b_planning = InlineKeyboardButton(text='Бронирование времени', callback_data='planning')
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
        builder.row(cls.b_planning)
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

    b_payment_robokassa = InlineKeyboardButton(text='Robokassa', callback_data='payment_robokassa')
    b_payment_yookassa = InlineKeyboardButton(text='ЮKassa', callback_data='payment_yookassa')

    b_back_to_payment = InlineKeyboardButton(text='Назад', callback_data='payment')

    @classmethod
    def payment(cls, url) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        robokassa =  InlineKeyboardButton(text='Robokassa', web_app=WebAppInfo(url=url))
        builder.add(robokassa, cls.b_payment_yookassa, cls.b_back_to_main)
        return builder.adjust(1).as_markup()

    @classmethod
    def back_to_payment(cls) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.add(cls.b_back_to_payment)
        return builder.as_markup()


class ShopKB(KB):
    b_buy = InlineKeyboardButton(text='💰 Купить', callback_data='buy_0')
    b_increace_amount = InlineKeyboardButton(text='+', callback_data='buy_1')
    b_decreace_amount = InlineKeyboardButton(text='-', callback_data='buy_-1')
    b_add_to_cart = InlineKeyboardButton(text='🛒 Добавить в корзину', callback_data='add_to_cart')

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
            back_to_shop_button: bool = False
    ) -> InlineKeyboardMarkup:

        builder = InlineKeyboardBuilder()
        for i, (id_, text) in enumerate(categories):
            if i % 2 == 0:
                builder.row(InlineKeyboardButton(text=text, callback_data=f'{prefix}_{id_}'))
            else:
                builder.add(InlineKeyboardButton(text=text, callback_data=f'{prefix}_{id_}'))
        if back_to_shop_button:
            builder.row(cls.b_shop)
        builder.row(cls.b_back_to_main)
        return builder.as_markup()

    @classmethod
    def item(cls) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.add(cls.b_buy, cls.b_add_to_cart, cls.b_shop, cls.b_back_to_main)
        return builder.adjust(1).as_markup()

    @classmethod
    def set_amount(cls) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.add(
            cls.b_buy,
            cls.b_decreace_amount,
            cls.b_increace_amount,
            cls.b_shop,
            cls.b_back_to_main
        )
        return builder.adjust(1, 2, 1).as_markup()

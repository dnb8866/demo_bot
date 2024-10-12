from datetime import datetime
from decimal import Decimal


import utils.assist as assist
from utils.models_orm import OrderItem, SlotDate

MONTH_TEXT = {
    1: 'Январь',
    2: 'Февраль',
    3: 'Март',
    4: 'Апрель',
    5: 'Май',
    6: 'Июнь',
    7: 'Июль',
    8: 'Август',
    9: 'Сентябрь',
    10: 'Октябрь',
    11: 'Ноябрь',
    12: 'Декабрь'
}


async def main(name):
    return (f'🔆 Здравствуйте, {name}!\n\n'
            f'Для оплаты услуг выберите "Оплата" 👇')


# def payment_description():
#     return ('На данной странице вы можете посмотреть возможности по интеграции различных сервисов оплаты в '
#             'телеграм-бота.\n\n'
#             'Предположим, что вы добавили в корзину или хотите приобрести какой-то товар/услугу.\n'
#             'Выберите ниже сервис, для демонстрации процесса оплаты.\n'
#             '👇')


async def shop():
    return '👇 Выберите раздел 👇'


async def items():
    return '👇 Выберите товар/услугу 👇'


async def item(name, description, price, quantity: int):
    return (f'� Название: {name}\n\n'
            f'� Описание: {description}\n\n'
            f'� Цена: {price} руб.\n\n'
            f'� Количество: {quantity}\n\n'
            f'� Для добавления товара в корзину нажмите "Добавить в корзину" 👇')


async def show_cart(order_items: list[OrderItem], total_price: Decimal):
    result = ['🛒 Ваша корзина 🛒\n']
    for order_item in order_items:
        res = (
            f'<u>{order_item.item.name}</u>',
            f'Цена: {str(order_item.item.price)}',
            f'Количество: {str(order_item.quantity)}',
            f'Сумма: {Decimal(str(order_item.item.price)) * order_item.quantity}\n'
        )
        result.append('\n'.join(res))
    result.append(f'<b><u>Общая сумма заказа: {total_price}</u></b>')
    return '\n'.join(result)


async def all_orders_from_user(orders: list):
    result = ['📋 Ваши заказы 📋\n']
    for order in orders:
        res = (
            f'<u>Заказ № {order.id}</u>',
            f'Статус: {order.status}',
            f'Дата создания: {order.created.strftime("%d.%m.%Y")}',
            f'Сумма заказа: {await assist.calculate_total_price_from_items(order.order_items)}\n'
        )
        result.append('\n'.join(res))
    return '\n'.join(result)


async def payment_description():
    return ('👇 Выберите способ оплаты 👇\n'
            'Для тестовой оплаты через Сбер используйте тестовую карту '
            '4111 1111 1111 1111, 12/24, CVC/CVV 123, проверочный код 12345678')


async def planner_welcome():
    return ('Планируйте свое время, записывайте клиентов в свободные слоты.\n\n'
            'Гибкая настройка под ваши потребности.')


async def planner_available_dates(
        current_month: tuple[SlotDate],
        next_month: tuple[SlotDate]
):
    dt = datetime.now()
    text = [
        f'Открытые даты для записи в текущем месяце ({MONTH_TEXT[dt.month]} {dt.year}):\n'
    ]
    temp = []
    for date in current_month:
        temp.append(str(date.slot_date.day))
    text.append(', '.join(temp))
    temp.clear()
    next_month_number = dt.month + 1 if dt.month < 12 else 1
    year = dt.year if dt.month < 12 else dt.year + 1
    text.append(
        f'\n\nОткрытые даты для записи в следующем месяце ({MONTH_TEXT[next_month_number]} {year}):\n'
    )
    for date in next_month:
        temp.append(str(date.slot_date.day))
    text.append(', '.join(temp))
    return ''.join(text)


def planner_choose_month():
    return '👇 Выберите месяц для редактирования расписания: 👇'


def planner_get_dates(type_operation):
    if type_operation == 'add':
        return '👇 Введите числа месяца (в эти дни для клиентов станет доступна запись) 👇'
    elif type_operation == 'remove':
        return '👇 Введите числа месяца (в эти дни для клиентов будет невозможна запись) 👇'


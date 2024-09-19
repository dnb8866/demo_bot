from decimal import Decimal


async def calculate_total_price_from_items(order_items: list):
    total = Decimal('0')
    for item in order_items:
        total += Decimal(str(item.item.price)) * item.quantity
    return total

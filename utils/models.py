from enum import Enum


class OrderStatus(Enum):
    CREATED = 'created'
    PAID = 'paid'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'


class SlotStatus(Enum):
    PENDING = 'pending'
    CANCELED = 'canceled'
    ACCEPTED = 'accepted'

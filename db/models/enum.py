from enum import Enum

class PaymentPeriod(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class PaymentMethod(str, Enum):
    EACH_USER = "from_each_user"
    TURN_RANDOM = "in_turn_randomly"
    TURN_JOIN_DATE = "in_turn_by_join_date"


class PaymentStatus(str, Enum):
    PAID = "paid"
    UNPAID = "unpaid"


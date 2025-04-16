from enum import Enum

class PaymentPeriod(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class PaymentMethod(str, Enum):
    FROM_EACH_USER = "from_each_user"
    IN_TURN_RANDOMLY = "in_turn_randomly"
    IN_TURN_BY_JOIN_DATE = "in_turn_by_join_date"


class PaymentStatus(str, Enum):
    PAID = "paid"
    UNPAID = "unpaid"


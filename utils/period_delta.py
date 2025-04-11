from datetime import timedelta

from config.settings import DAYS_IN_SUBSCRIPTION_MONTH
from db.models import PaymentPeriod


def get_period_delta(period: PaymentPeriod) -> timedelta:
    return {
        PaymentPeriod.DAILY: timedelta(days=1),
        PaymentPeriod.WEEKLY: timedelta(weeks=1),
        PaymentPeriod.MONTHLY: timedelta(days=DAYS_IN_SUBSCRIPTION_MONTH),
    }[period]

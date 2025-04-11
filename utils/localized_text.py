from translation import localize_text
from utils import get_displayed_date


def get_localized_group_user(group, user) -> str:
    return localize_text(
        'messages.group_user_list',
        user_id=user.user_tag if user.user_tag else user.user_id,
        join_date=get_displayed_date(user.joined_at),
        date=get_displayed_date(group.get_next_payment_date(user)),
        status=localize_text(f"buttons.{user.status.replace('.PaymentStatus.', '')}"),
        pay_date = get_displayed_date(user.last_payment_date) if user.last_payment_date else localize_text('messages.never')
    )

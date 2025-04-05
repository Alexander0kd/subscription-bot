import string
from datetime import datetime
from random import choice

from bson import ObjectId

UA_MONTH_NAMES = [
    "Січня", "Лютого", "Березня", "Квітня",
    "Травня", "Червня", "Липня", "Серпня",
    "Вересня", "Жовтня", "Листопада", "Грудня"
]


def get_object_id(share_id: str) -> ObjectId:
    """Convert a shareable group ID to MongoDB ObjectId"""
    return ObjectId(share_id)


def generate_join_id(length: int = 16) -> str:
    """Generate a random alphanumeric join ID"""
    res = ''
    characters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    for i in range(length // 4):
        res += ''.join(choice(characters) for _ in range(length // 4))
        if i != length // 4 - 1:
            res += '-'
    return res

def get_displayed_date(date: datetime) -> str:
    """Format date as '04 Квітня' (day + month name in Ukrainian)"""
    day = date.strftime('%d')
    day = day if not day.startswith('0') else f'{day.replace("0", "")}'

    month_idx = date.month - 1  # 0-based index for our list
    month_name = UA_MONTH_NAMES[month_idx]

    return f"{day} {month_name}"
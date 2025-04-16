from datetime import datetime

UA_MONTH_NAMES = [
    "Січня", "Лютого", "Березня", "Квітня",
    "Травня", "Червня", "Липня", "Серпня",
    "Вересня", "Жовтня", "Листопада", "Грудня"
]

def get_displayed_date(date: datetime) -> str:
    day = date.strftime('%d')
    day = day if not day.startswith('0') else f'{day.replace("0", "")}'

    month_idx = date.month - 1
    month_name = UA_MONTH_NAMES[month_idx]

    return f"{day} {month_name}"


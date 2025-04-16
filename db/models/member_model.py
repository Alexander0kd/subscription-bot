from typing import Dict, Optional, Union, Any
from datetime import datetime
from bson import ObjectId

from db.models import PaymentStatus

class MemberModel:
    def __init__(
            self,
            user_id: int,
            user_tag: str,
            last_payment_date: Optional[datetime],
            status: PaymentStatus,
            joined_at: datetime,
            _id: Optional[Union[str, ObjectId]] = None
    ):
        self.user_id = user_id
        self.user_tag = user_tag
        self.last_payment_date = last_payment_date
        self.status = status or PaymentStatus.UNPAID
        self.joined_at = joined_at or datetime.now()
        self._id = ObjectId(_id) if _id and isinstance(_id, str) else _id

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MemberModel':
        _id = data.get('_id')

        status = data.get('status')
        if isinstance(status, str):
            data['status'] = PaymentStatus(status)

        last_payment_date = data.get('last_payment_date')
        if isinstance(last_payment_date, str):
            data['last_payment_date'] = datetime.fromisoformat(last_payment_date)

        joined_at = data.get('joined_at')
        if isinstance(joined_at, str):
            data['joined_at'] = datetime.fromisoformat(joined_at)

        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        result = {
            'user_id': self.user_id,
            'user_tag': self.user_tag,
            'last_payment_date': self.last_payment_date,
            'status': self.status.value if isinstance(self.status, PaymentStatus) else self.status,
            'joined_at': self.joined_at,
        }

        if self._id:
            result['_id'] = self._id

        return result

    def __str__(self) -> str:
        return f"Member(id={self.user_id}, user_tag={self.user_tag}, last_payment_date={self.last_payment_date}, status={self.status}, joined_at={self.joined_at})"

def get_default_member(user_id: int, user_tag: str) -> MemberModel:
    return MemberModel(user_id=user_id, user_tag=user_tag, last_payment_date=None, status=PaymentStatus.UNPAID, joined_at=datetime.now())
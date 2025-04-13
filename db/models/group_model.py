from typing import List, Dict, Optional, Union, Any
from datetime import datetime
from bson import ObjectId

from db.models import PaymentPeriod, PaymentMethod, PaymentStatus
from db.models.member_model import MemberModel, get_default_member
from db.utils import generate_join_id
from utils import get_period_delta


class GroupModel:
    """Model representing a payment group in the database"""

    def __init__(
            self,
            name: str,
            owner_id: int,
            owner_tag: str,
            description: Optional[str] = None,
            amount: float = 0.0,
            payment_period: PaymentPeriod = PaymentPeriod.MONTHLY,
            payment_method: PaymentMethod = PaymentMethod.EACH_USER,
            current_payment_date: Optional[datetime] = None,
            next_payment_date: Optional[datetime] = None,
            members: Optional[List[MemberModel]] = None,
            created_at: Optional[datetime] = None,
            join_id: Optional[str] = None,
            _id: Optional[Union[str, ObjectId]] = None
    ):
        self.name = name
        self.owner_id = owner_id
        self.owner_tag = owner_tag
        self.description = description
        self.amount = amount
        self.payment_period = payment_period
        self.payment_method = payment_method
        self.current_payment_date = current_payment_date or datetime.now()
        self.next_payment_date = next_payment_date or datetime.now()
        self.members = members or []
        self.created_at = created_at or datetime.now()
        self.join_id = join_id or generate_join_id()
        self._id = ObjectId(_id) if _id and isinstance(_id, str) else _id


    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GroupModel':
        """Create a GroupModel instance from a dictionary"""
        # Handle ObjectId conversion
        _id = data.get('_id')

        # Handle enum conversion
        payment_period = data.get('payment_period')
        if isinstance(payment_period, str):
            data['payment_period'] = PaymentPeriod(payment_period)

        payment_method = data.get('payment_method')
        if isinstance(payment_method, str):
            data['payment_method'] = PaymentMethod(payment_method)

        # Convert datetime strings if needed
        current_payment_date = data.get('current_payment_date')
        if isinstance(current_payment_date, str):
            data['current_payment_date'] = datetime.fromisoformat(current_payment_date)

        next_payment_date = data.get('next_payment_date')
        if isinstance(next_payment_date, str):
            data['next_payment_date'] = datetime.fromisoformat(next_payment_date)

        created_at = data.get('created_at')
        if isinstance(created_at, str):
            data['created_at'] = datetime.fromisoformat(created_at)

        # Handle members conversion if needed
        if 'members' in data:
            data['members'] = [MemberModel.from_dict(m) for m in data['members']]

        # Handle payment history conversion if needed
        if 'payment_history' in data:
            for payment in data['payment_history']:
                if 'date' in payment and isinstance(payment['date'], str):
                    payment['date'] = datetime.fromisoformat(payment['date'])

        return cls(**data)


    def to_dict(self) -> Dict[str, Any]:
        """Convert the model to a dictionary for database storage"""
        result = {
            'name': self.name,
            'owner_id': self.owner_id,
            'owner_tag': self.owner_tag,
            'description': self.description,
            'amount': self.amount,
            'payment_period': self.payment_period.value if isinstance(self.payment_period,
                                                                      PaymentPeriod) else self.payment_period,
            'payment_method': self.payment_method.value if isinstance(self.payment_method,
                                                                      PaymentMethod) else self.payment_method,
            'current_payment_date': self.current_payment_date,
            'next_payment_date': self.next_payment_date,

            'members': [m.to_dict() for m in self.members],
            'created_at': self.created_at,
            'join_id': self.join_id
        }

        if self._id:
            result['_id'] = self._id

        return result


    def get_next_payment_date(self, user: MemberModel) -> datetime:
        """Calculate the next payment date for a user"""
        import hashlib

        period_delta = get_period_delta(self.payment_period)

        if self.payment_method == PaymentMethod.EACH_USER:
            return self.current_payment_date

        elif self.payment_method in [PaymentMethod.TURN_JOIN_DATE, PaymentMethod.TURN_RANDOM]:
            members = list(self.members)

            if self.payment_method == PaymentMethod.TURN_JOIN_DATE:
                members.sort(key=lambda m: m.joined_at)
                members.reverse()
            else:
                def stable_hash(u: int) -> int:
                    return int(hashlib.md5(str(u).encode()).hexdigest(), 16)

                members.sort(key=lambda m: stable_hash(m.user_id))

            try:
                index = next(i for i, m in enumerate(members) if m.user_id == user.user_id)
            except StopIteration:
                return self.current_payment_date

            base_date = self.current_payment_date
            return base_date + index * period_delta

        return self.current_payment_date


    def add_member(self, user_id: int, user_tag: str):
        """Add a new member to the group if they don't already exist."""

        def _find_member(find_user_id: int) -> Optional[MemberModel]:
            """Helper function to find a member by user_id in the members list."""
            return next((m for m in self.members if m.user_id == find_user_id), None)

        existing_member = _find_member(user_id)
        if not existing_member:
            new_member = get_default_member(user_id, user_tag)
            self.members.append(new_member)


    def __str__(self) -> str:
        """String representation of the group"""
        return f"Group(name={self.name}, owner_id={self.owner_id}, members={len(self.members)})"
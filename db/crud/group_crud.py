from datetime import datetime
from typing import Optional, List
from pymongo.errors import PyMongoError
from pymongo.results import InsertOneResult

from db.models import PaymentStatus, MemberModel, get_default_member
from db.models.group_model import GroupModel
from db import get_db


db = get_db()
COLLECTION_NAME = GroupModel.__name__


async def get_group_by_join_id(join_id: str) -> Optional[GroupModel]:
    try:
        group_data = db[COLLECTION_NAME].find_one({"join_id": join_id})
        if group_data:
            return GroupModel.from_dict(dict(group_data))
        return None
    except PyMongoError as e:
        print(f"Error getting group by ID: {str(e)}")
        return None


async def create_group_with_custom_join_id(group: GroupModel) -> Optional[str]:
    try:
        existing = await get_group_by_join_id(group.join_id)
        if existing:
            raise ValueError(f"Join ID '{group.join_id}' is already in use")

        result: InsertOneResult = db[COLLECTION_NAME].insert_one(group.to_dict())
        return str(result.inserted_id) if result.inserted_id else None
    except PyMongoError as e:
        print(f"Error creating group with custom join ID: {str(e)}")
        return None


async def get_by_owner(owner_id: int) -> List[GroupModel]:
    group_data = db[COLLECTION_NAME].find({"owner_id": owner_id})
    return [GroupModel.from_dict(dict(g)) for g in group_data]


async def get_by_member(member_id: int) -> List[GroupModel]:
    group_data = db[COLLECTION_NAME].find({
        "members.user_id": member_id
    })

    converted = [GroupModel.from_dict(dict(g)) for g in group_data]

    result = []
    for group in converted:
        members = group.members or []

        main_member = [m for m in members if str(m.user_id) == str(member_id)]
        other_members = [m for m in members if str(m.user_id) != str(member_id)]

        group.members = main_member + other_members
        result.append(group)

    return result


async def leave_group(group: GroupModel, user_id: int):
    group.members = [member for member in group.members if str(member.user_id) != str(user_id)]
    await update_group(group)


async def mark_payment(group: GroupModel, user_id: int, toggle: bool = False):
    group.members = sorted(group.members, key=lambda m: 1 if str(m.user_id) == str(user_id) else 0, reverse=True)

    if group.members and len(group.members) > 0:
        if toggle:
            group.members[0].status = (
                PaymentStatus.UNPAID if group.members[0].status == PaymentStatus.PAID else PaymentStatus.PAID
            )
        else:
            group.members[0].status = PaymentStatus.PAID
            group.members[0].last_payment_date = datetime.now()

    await update_group(group)


async def update_group(group: GroupModel):
   db[COLLECTION_NAME].update_one(
        {"join_id": group.join_id},
        {"$set": group.to_dict()}
    )


async def delete_group(group: GroupModel):
    db[COLLECTION_NAME].delete_one({"join_id": group.join_id})


async def add_member(group: GroupModel, user_id: int, user_tag: str):
    def _find_member(find_user_id: int) -> Optional[MemberModel]:
        return next((m for m in group.members if str(m.user_id) == str(find_user_id)), None)

    existing_member = _find_member(user_id)
    if not existing_member:
        new_member = get_default_member(user_id, user_tag)
        group.members.append(new_member)
        await update_group(group)


async def get_all_groups_by_date(date: datetime = datetime.now()) -> List[GroupModel]:
    group_data = db[COLLECTION_NAME].find({ "current_payment_date": { "$lte": date } })
    return [GroupModel.from_dict(dict(g)) for g in group_data]


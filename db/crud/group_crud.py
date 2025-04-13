from datetime import datetime
from typing import Optional, List
from pymongo.errors import PyMongoError
from pymongo.results import InsertOneResult

from db.models import PaymentStatus
from db.models.group_model import GroupModel
from db import get_db


db = get_db()
COLLECTION_NAME = GroupModel.__name__


async def get_group_by_join_id(join_id: str) -> Optional[GroupModel]:
    """
    Get a group by its ID

    Args:
        join_id: The ID of the group to get

    Returns:
        Optional[GroupModel]: The group if found, None otherwise
    """
    try:
        group_data = db[COLLECTION_NAME].find_one({"join_id": join_id})
        if group_data:
            return GroupModel.from_dict(dict(group_data))
        return None
    except PyMongoError as e:
        print(f"Error getting group by ID: {str(e)}")
        return None


async def create_group_with_custom_join_id(group: GroupModel) -> Optional[str]:
    """
    Create a new group with a custom join ID

    Args:
        group: The group to create

    Returns:
        Optional[str]: The ID of the new group if successful, None otherwise

    Raises:
        ValueError: If the custom join ID is already in use
    """
    try:
        # Check if join_id already exists
        existing = await get_group_by_join_id(group.join_id)
        if existing:
            raise ValueError(f"Join ID '{group.join_id}' is already in use")

        result: InsertOneResult = db[COLLECTION_NAME].insert_one(group.to_dict())
        return str(result.inserted_id) if result.inserted_id else None
    except PyMongoError as e:
        print(f"Error creating group with custom join ID: {str(e)}")
        return None


async def get_by_owner(owner_id: int) -> List[GroupModel]:
    """Отримати групи за власником"""
    group_data = db[COLLECTION_NAME].find({"owner_id": owner_id})
    return [GroupModel.from_dict(dict(g)) for g in group_data]


async def get_by_member(member_id: int) -> List[GroupModel]:
    """Отримати групи за учасником"""
    group_data = db[COLLECTION_NAME].find({
        "members.user_id": member_id,
        "owner_id": {"$ne": member_id}
    })

    converted = [GroupModel.from_dict(dict(g)) for g in group_data]

    result = []
    for group in converted:
        members = group.members or []

        main_member = [m for m in members if m.user_id == member_id]
        other_members = [m for m in members if m.user_id != member_id]

        group.members = main_member + other_members
        result.append(group)

    return result


async def leave_group(group: GroupModel, user_id: int):
    group.members = [member for member in group.members if member.user_id != user_id]
    await update_group(group)


async def mark_payment(group: GroupModel, user_id: int, toggle: bool = False):
    group.members.sort(key=lambda m: 0 if m.user_id == user_id else 1)

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

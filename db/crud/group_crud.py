from typing import Optional, List
from pymongo.errors import PyMongoError
from pymongo.results import InsertOneResult

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

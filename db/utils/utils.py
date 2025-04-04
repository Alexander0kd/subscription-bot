import string
from random import choice

from bson import ObjectId


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

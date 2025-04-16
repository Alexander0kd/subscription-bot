from config import MONGO_URI, MONGO_DB_NAME
from typing import Optional
from pymongo import MongoClient
from pymongo.database import Database

_db_client: Optional[MongoClient] = None
_db: Optional[Database] = None

def connect_to_db() -> Database:
    global _db_client, _db

    if _db is not None:
        return _db

    try:
        if not MONGO_URI:
            raise ValueError("MongoDB connection string not found. Set MONGO_URI environment variable.")

        _db_client = MongoClient(MONGO_URI)

        _db = _db_client[MONGO_DB_NAME]

        _db.command("ping")
        print(f"Successfully connected to MongoDB database: {MONGO_DB_NAME}")

        return _db

    except Exception as e:
        raise ConnectionError(f"Could not connect to MongoDB: {str(e)}")

def get_db() -> Database:
    global _db
    if _db is None:
        _db = connect_to_db()
    return _db

def close_db_connection():
    global _db_client, _db
    if _db_client is not None:
        _db_client.close()
        _db_client = None
        _db = None

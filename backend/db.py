from typing import Any

from pymongo import MongoClient

from config import DATABASE_NAME, MONGODB_URI


_client: MongoClient | None = None


def getClient() -> MongoClient:
    global _client
    if _client is None:
        _client = MongoClient(MONGODB_URI)
    return _client


def getDatabase() -> Any:
    client = getClient()
    return client[DATABASE_NAME]

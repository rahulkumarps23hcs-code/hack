import json
from pathlib import Path

from pymongo import MongoClient

from config import DATABASE_NAME, MONGODB_URI


def getProjectRoot() -> Path:
    return Path(__file__).resolve().parents[1]


def getCleanDataDir() -> Path:
    return getProjectRoot() / "data-engineering" / "clean-data"


def seedCollection(client: MongoClient, name: str, fileName: str) -> None:
    db = client[DATABASE_NAME]
    path = getCleanDataDir() / fileName
    if not path.exists():
        print(f"[WARN] File not found, skipping: {path}")
        return
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise ValueError(f"Expected list in {path}, got {type(data)}")
    if not data:
        print(f"[INFO] No documents in {path}, skipping.")
        return
    collection = db[name]
    collection.delete_many({})
    result = collection.insert_many(data)
    print(f"[INFO] Seeded {len(result.inserted_ids)} docs into {DATABASE_NAME}.{name}")


def main() -> None:
    client = MongoClient(MONGODB_URI)
    try:
        seedCollection(client, "alerts", "alerts.json")
        seedCollection(client, "safespots", "safe-spots.json")
        seedCollection(client, "users", "users.json")
    finally:
        client.close()


if __name__ == "__main__":
    main()

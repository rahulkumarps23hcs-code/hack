from pymongo import ASCENDING, MongoClient, GEOSPHERE

from config import DATABASE_NAME, MONGODB_URI


def main() -> None:
    client = MongoClient(MONGODB_URI)
    try:
        db = client[DATABASE_NAME]
        alerts = db.alerts
        safespots = db.safespots
        users = db.users

        alerts.create_index([("location", GEOSPHERE)])
        print("[INFO] Created 2dsphere index on alerts.location")

        safespots.create_index([("location", GEOSPHERE)])
        print("[INFO] Created 2dsphere index on safespots.location")

        users.create_index([("id", ASCENDING)], unique=True)
        print("[INFO] Created unique index on users.id")
    finally:
        client.close()


if __name__ == "__main__":
    main()

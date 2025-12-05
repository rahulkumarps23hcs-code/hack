"""Validation script for SAFE-ZONE clean datasets.

Checks:
- required fields present
- lat/lng valid ranges
- timestamp ISO-parseable
- id uniqueness
"""

from pathlib import Path

import pandas as pd


def getBaseDir() -> Path:
    return Path(__file__).resolve().parent.parent


def getCleanDir() -> Path:
    return getBaseDir() / "clean-data"


def validateAlerts(df: pd.DataFrame) -> None:
    required = ["id", "type", "severity", "timestamp", "location.lat", "location.lng", "description"]
    missingCols = [c for c in required if c not in df.columns]
    if missingCols:
        print("[ERROR] alerts.csv missing columns:", missingCols)
    lat = df["location.lat"].astype(float)
    lng = df["location.lng"].astype(float)
    invalid = (~lat.between(-90, 90)) | (~lng.between(-180, 180))
    print(f"[INFO] alerts invalid coordinates rows: {int(invalid.sum())}")
    ts = pd.to_datetime(df["timestamp"], errors="coerce", utc=True)
    invalidTs = ts.isna()
    print(f"[INFO] alerts invalid timestamps: {int(invalidTs.sum())}")
    duplicates = df["id"].duplicated().sum()
    print(f"[INFO] alerts duplicate ids: {int(duplicates)}")


def validateSafeSpots(df: pd.DataFrame) -> None:
    required = ["id", "name", "type", "address", "location.lat", "location.lng"]
    missingCols = [c for c in required if c not in df.columns]
    if missingCols:
        print("[ERROR] safe-spots.csv missing columns:", missingCols)
    lat = df["location.lat"].astype(float)
    lng = df["location.lng"].astype(float)
    invalid = (~lat.between(-90, 90)) | (~lng.between(-180, 180))
    print(f"[INFO] safe-spots invalid coordinates rows: {int(invalid.sum())}")
    duplicates = df["id"].duplicated().sum()
    print(f"[INFO] safe-spots duplicate ids: {int(duplicates)}")


def validateUsers(df: pd.DataFrame) -> None:
    required = ["id", "name", "phone", "email"]
    missingCols = [c for c in required if c not in df.columns]
    if missingCols:
        print("[ERROR] users.csv missing columns:", missingCols)
    duplicates = df["id"].duplicated().sum()
    print(f"[INFO] users duplicate ids: {int(duplicates)}")


def main() -> None:
    cleanDir = getCleanDir()

    alertsPath = cleanDir / "alerts.csv"
    safeSpotsPath = cleanDir / "safe-spots.csv"
    usersPath = cleanDir / "users.csv"

    if alertsPath.exists():
        alertsDf = pd.read_csv(alertsPath)
        print("=== Validating alerts.csv ===")
        validateAlerts(alertsDf)
    else:
        print("[WARN] alerts.csv not found")

    if safeSpotsPath.exists():
        safeSpotsDf = pd.read_csv(safeSpotsPath)
        print("=== Validating safe-spots.csv ===")
        validateSafeSpots(safeSpotsDf)
    else:
        print("[WARN] safe-spots.csv not found")

    if usersPath.exists():
        usersDf = pd.read_csv(usersPath)
        print("=== Validating users.csv ===")
        validateUsers(usersDf)
    else:
        print("[WARN] users.csv not found")


if __name__ == "__main__":
    main()

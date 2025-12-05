import json
import sys
from pathlib import Path
from typing import Optional

import pandas as pd

currentDir = Path(__file__).resolve().parent
utilsDir = currentDir.parent / "utils"
if str(utilsDir) not in sys.path:
    sys.path.insert(0, str(utilsDir))

from logger import getLogger

import crime_data_cleaner
import sos_reports_cleaner
import street_light_preprocessor


logger = getLogger(__name__)


def getBaseDir() -> Path:
    return Path(__file__).resolve().parent.parent


def getRawDir() -> Path:
    return getBaseDir() / "raw-data"


def getCleanDir() -> Path:
    cleanDir = getBaseDir() / "clean-data"
    cleanDir.mkdir(parents=True, exist_ok=True)
    return cleanDir


def buildAlertsFromFrames(
    crimeDf: Optional[pd.DataFrame] = None,
    sosDf: Optional[pd.DataFrame] = None,
) -> pd.DataFrame:
    parts = []
    if crimeDf is not None and not crimeDf.empty:
        parts.append(crime_data_cleaner.convertCrimeToAlerts(crimeDf))
    if sosDf is not None and not sosDf.empty:
        parts.append(sos_reports_cleaner.convertSosToAlerts(sosDf))
    if not parts:
        return pd.DataFrame(columns=["id", "type", "severity", "timestamp", "lat", "lng", "description"])
    alerts = pd.concat(parts, ignore_index=True)
    alerts = alerts.drop_duplicates(subset=["id"]).reset_index(drop=True)
    logger.info("Built alerts frame from sources; shape=%s", alerts.shape)
    return alerts


def buildSafeSpotsFromFrame(streetDf: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    if streetDf is None or streetDf.empty:
        return pd.DataFrame(columns=["id", "name", "type", "address", "lat", "lng"])
    safeSpots = street_light_preprocessor.convertLightsToSafeSpots(streetDf)
    safeSpots = safeSpots.drop_duplicates(subset=["id"]).reset_index(drop=True)
    logger.info("Built safe spots frame from street lights; shape=%s", safeSpots.shape)
    return safeSpots


def buildDemoAlerts() -> pd.DataFrame:
    df = pd.DataFrame(
        {
            "id": ["A001", "A002"],
            "type": ["harassment", "theft"],
            "severity": ["high", "medium"],
            "timestamp": [
                "2025-01-01T23:21:00Z",
                "2025-01-01T23:45:00Z",
            ],
            "lat": [26.9124, 26.9150],
            "lng": [75.7873, 75.7890],
            "description": [
                "Night-time harassment report",
                "Bag snatched near bus stop",
            ],
        }
    )
    return df


def buildDemoSafeSpots() -> pd.DataFrame:
    df = pd.DataFrame(
        {
            "id": ["S001", "S002"],
            "name": ["Police Station Central", "City Hospital"],
            "type": ["police-station", "hospital"],
            "address": ["MG Road, City Center", "Ring Road, Sector 5"],
            "lat": [26.9129, 26.9180],
            "lng": [75.7878, 75.7920],
        }
    )
    return df


def buildDemoUsers(count: int = 20) -> pd.DataFrame:
    rows = []
    for index in range(1, count + 1):
        userId = f"U{index:03d}"
        name = f"User {index:03d}"
        phone = f"+91-99999-{index:04d}"
        email = f"user{index:03d}@safezone.local"
        rows.append({"id": userId, "name": name, "phone": phone, "email": email})
    return pd.DataFrame(rows)


def writeAlertsArtifacts(alerts: pd.DataFrame) -> None:
    cleanDir = getCleanDir()
    if alerts.empty:
        logger.warning("Alerts frame is empty; nothing to write.")
        return
    csvDf = alerts.copy()
    csvDf["location.lat"] = csvDf["lat"]
    csvDf["location.lng"] = csvDf["lng"]
    csvDf = csvDf[
        [
            "id",
            "type",
            "severity",
            "timestamp",
            "location.lat",
            "location.lng",
            "description",
        ]
    ]
    csvPath = cleanDir / "alerts.csv"
    csvDf.to_csv(csvPath, index=False)
    logger.info("Wrote alerts CSV to %s", csvPath)
    records = []
    for row in alerts.itertuples(index=False):
        record = {
            "id": row.id,
            "type": row.type,
            "severity": row.severity,
            "timestamp": row.timestamp,
            "location": {"lat": float(row.lat), "lng": float(row.lng)},
            "description": row.description,
        }
        records.append(record)
    jsonPath = cleanDir / "alerts.json"
    jsonPath.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info("Wrote alerts JSON to %s", jsonPath)


def writeSafeSpotsArtifacts(safeSpots: pd.DataFrame) -> None:
    cleanDir = getCleanDir()
    if safeSpots.empty:
        logger.warning("Safe spots frame is empty; nothing to write.")
        return
    csvDf = safeSpots.copy()
    csvDf["location.lat"] = csvDf["lat"]
    csvDf["location.lng"] = csvDf["lng"]
    csvDf = csvDf[["id", "name", "type", "address", "location.lat", "location.lng"]]
    csvPath = cleanDir / "safe-spots.csv"
    csvDf.to_csv(csvPath, index=False)
    logger.info("Wrote safe spots CSV to %s", csvPath)
    records = []
    for row in safeSpots.itertuples(index=False):
        record = {
            "id": row.id,
            "name": row.name,
            "type": row.type,
            "address": row.address,
            "location": {"lat": float(row.lat), "lng": float(row.lng)},
        }
        records.append(record)
    jsonPath = cleanDir / "safe-spots.json"
    jsonPath.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info("Wrote safe spots JSON to %s", jsonPath)


def writeUsersArtifacts(users: pd.DataFrame) -> None:
    cleanDir = getCleanDir()
    if users.empty:
        logger.warning("Users frame is empty; nothing to write.")
        return
    csvPath = cleanDir / "users.csv"
    users.to_csv(csvPath, index=False)
    logger.info("Wrote users CSV to %s", csvPath)
    records = [row._asdict() for row in users.itertuples(index=False)]
    jsonPath = cleanDir / "users.json"
    jsonPath.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info("Wrote users JSON to %s", jsonPath)


def runDemoPipeline() -> None:
    demoAlerts = buildDemoAlerts()
    demoSafeSpots = buildDemoSafeSpots()
    demoUsers = buildDemoUsers()
    writeAlertsArtifacts(demoAlerts)
    writeSafeSpotsArtifacts(demoSafeSpots)
    writeUsersArtifacts(demoUsers)


if __name__ == "__main__":
    logger.info("Running SAFE-ZONE data engineering demo pipeline.")
    runDemoPipeline()
    logger.info("Demo pipeline finished. Check the 'clean-data' folder for outputs.")

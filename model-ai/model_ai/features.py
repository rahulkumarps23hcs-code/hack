from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd


def getProjectRoot() -> Path:
    return Path(__file__).resolve().parents[2]


def getCleanDataDir() -> Path:
    return getProjectRoot() / "data-engineering" / "clean-data"


def loadAlerts(cleanDir: Path | None = None) -> pd.DataFrame:
    baseDir = cleanDir or getCleanDataDir()
    csvPath = baseDir / "alerts.csv"
    if not csvPath.exists():
        raise FileNotFoundError(f"alerts.csv not found in {baseDir}")
    df = pd.read_csv(csvPath)
    if "location.lat" in df.columns and "location.lng" in df.columns:
        df["lat"] = df["location.lat"].astype(float)
        df["lng"] = df["location.lng"].astype(float)
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce", utc=True)
    df = df.dropna(subset=["timestamp", "lat", "lng"])
    return df


def buildUnsafeZoneFeatures(alerts: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
    data = alerts.copy()
    dt = data["timestamp"].dt
    data["hour"] = dt.hour
    data["dayOfWeek"] = dt.dayofweek
    severityMap = {"low": 0, "medium": 1, "high": 2}
    data["severityCode"] = (
        data["severity"].astype(str).str.lower().map(severityMap).fillna(1).astype(int)
    )
    features = data[["lat", "lng", "hour", "dayOfWeek", "severityCode"]].to_numpy(dtype=float)
    labels = (data["severity"].astype(str).str.lower() == "high").astype(int).to_numpy()
    return features, labels


def buildSosRiskFeatures(alerts: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
    data = alerts.copy()
    dt = data["timestamp"].dt
    data["hour"] = dt.hour
    data["messageLength"] = data["description"].fillna("").astype(str).str.len()
    data["isNight"] = ((data["hour"] >= 20) | (data["hour"] <= 5)).astype(int)
    severityMap = {"low": 0, "medium": 1, "high": 2}
    data["severityCode"] = (
        data["severity"].astype(str).str.lower().map(severityMap).fillna(1).astype(int)
    )
    features = data[["hour", "messageLength", "isNight", "severityCode"]].to_numpy(dtype=float)
    labels = (data["severity"].astype(str).str.lower() == "high").astype(int).to_numpy()
    return features, labels

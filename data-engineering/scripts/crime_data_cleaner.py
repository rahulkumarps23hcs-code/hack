import sys
from pathlib import Path
from typing import Any, Optional

import pandas as pd

currentDir = Path(__file__).resolve().parent
utilsDir = currentDir.parent / "utils"
if str(utilsDir) not in sys.path:
    sys.path.insert(0, str(utilsDir))

from logger import getLogger
from geospatial_utils import filterInvalidCoordinates


logger = getLogger(__name__)


def loadCrimeData(filePath: str, **readKwargs: Any) -> pd.DataFrame:
    path = Path(filePath)
    suffix = path.suffix.lower()
    if suffix == ".json":
        df = pd.read_json(path, **readKwargs)
    elif suffix == ".parquet":
        df = pd.read_parquet(path, **readKwargs)
    else:
        df = pd.read_csv(path, **readKwargs)
    logger.info("Loaded crime data from %s with shape %s", path, df.shape)
    return df


def convertCrimeToAlerts(
    df: pd.DataFrame,
    idCol: Optional[str] = "id",
    typeCol: str = "type",
    severityCol: str = "severity",
    timestampCol: str = "timestamp",
    latCol: str = "lat",
    lngCol: str = "lng",
    descriptionCol: str = "description",
    idPrefix: str = "A",
) -> pd.DataFrame:
    data = df.copy()
    if timestampCol in data.columns:
        timestampSeries = pd.to_datetime(data[timestampCol], errors="coerce", utc=True)
        maskValid = timestampSeries.notna()
        data = data.loc[maskValid].copy()
        data["timestamp"] = timestampSeries.loc[maskValid].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    else:
        logger.warning("Timestamp column '%s' not found in crime data.", timestampCol)
        return pd.DataFrame(columns=["id", "type", "severity", "timestamp", "lat", "lng", "description"])
    if typeCol in data.columns:
        typeSeries = data[typeCol].astype(str).str.strip().str.lower()
        typeSeries = typeSeries.replace("nan", pd.NA)
        data["type"] = typeSeries.fillna("unknown")
    else:
        data["type"] = "unknown"
    if severityCol in data.columns:
        severitySeries = data[severityCol].astype(str).str.strip().str.lower()
        severitySeries = severitySeries.replace("nan", pd.NA)
        data["severity"] = severitySeries.fillna("medium")
    else:
        data["severity"] = "medium"
    if descriptionCol in data.columns:
        descSeries = data[descriptionCol].fillna("").astype(str)
        descSeries = descSeries.str.replace(r"\s+", " ", regex=True).str.strip()
        data["description"] = descSeries
    else:
        data["description"] = ""
    data = data[data["description"] != ""]
    if latCol in data.columns and lngCol in data.columns:
        data = filterInvalidCoordinates(data, latCol=latCol, lngCol=lngCol)
        data = data.dropna(subset=[latCol, lngCol])
        data["lat"] = data[latCol].astype(float)
        data["lng"] = data[lngCol].astype(float)
    else:
        logger.warning(
            "Latitude/longitude columns '%s'/'%s' not found; returning empty alerts frame.",
            latCol,
            lngCol,
        )
        return pd.DataFrame(columns=["id", "type", "severity", "timestamp", "lat", "lng", "description"])
    if idCol and idCol in data.columns:
        idSeries = data[idCol].astype(str).str.strip()
        idSeries = idSeries.replace("", pd.NA)
    else:
        idSeries = pd.Series(pd.NA, index=data.index)
    missingMask = idSeries.isna()
    if missingMask.any():
        countMissing = int(missingMask.sum())
        generated = [f"{idPrefix}{i:03d}" for i in range(1, countMissing + 1)]
        idSeries.loc[missingMask] = generated
    data["id"] = idSeries.astype(str)
    result = data[["id", "type", "severity", "timestamp", "lat", "lng", "description"]].reset_index(drop=True)
    logger.info("Converted crime data to alerts format; shape=%s", result.shape)
    return result


if __name__ == "__main__":
    sample = pd.DataFrame(
        {
            "id": [1, 2, 2],
            "type": ["robbery", "ASSAULT", None],
            "severity": ["high", "medium", None],
            "timestamp": [
                "2025-01-01 10:00:00",
                "2025-01-01 10:10:00",
                "2025-01-01 10:10:00",
            ],
            "lat": [26.9124, 26.9150, 26.9150],
            "lng": [75.7873, 75.7890, 75.7890],
            "description": [
                "wallet stolen near market",
                "street fight reported",
                None,
            ],
        }
    )
    logger.info("Raw crime sample:\n%s", sample)
    alertsSample = convertCrimeToAlerts(sample)
    logger.info("Alerts derived from crime sample:\n%s", alertsSample)

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


def loadSosReports(filePath: str, **readKwargs: Any) -> pd.DataFrame:
    path = Path(filePath)
    suffix = path.suffix.lower()
    if suffix == ".json":
        df = pd.read_json(path, **readKwargs)
    elif suffix == ".parquet":
        df = pd.read_parquet(path, **readKwargs)
    else:
        df = pd.read_csv(path, **readKwargs)
    logger.info("Loaded SOS reports from %s with shape %s", path, df.shape)
    return df


def cleanTextColumn(series: pd.Series) -> pd.Series:
    cleaned = series.fillna("").astype(str)
    cleaned = cleaned.str.replace(r"\s+", " ", regex=True).str.strip().str.lower()
    cleaned = cleaned.replace("", pd.NA)
    return cleaned


def convertSosToAlerts(
    df: pd.DataFrame,
    idCol: Optional[str] = "id",
    messageCol: str = "message",
    typeCol: Optional[str] = "type",
    severityCol: Optional[str] = "severity",
    timestampCol: str = "timestamp",
    latCol: str = "lat",
    lngCol: str = "lng",
    idPrefix: str = "S",
) -> pd.DataFrame:
    data = df.copy()
    if timestampCol in data.columns:
        timestampSeries = pd.to_datetime(data[timestampCol], errors="coerce", utc=True)
        maskValid = timestampSeries.notna()
        data = data.loc[maskValid].copy()
        data["timestamp"] = timestampSeries.loc[maskValid].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    else:
        logger.warning("Timestamp column '%s' not found in SOS reports.", timestampCol)
        return pd.DataFrame(columns=["id", "type", "severity", "timestamp", "lat", "lng", "description"])
    if messageCol in data.columns:
        descriptionSeries = cleanTextColumn(data[messageCol])
    else:
        descriptionSeries = pd.Series("sos alert", index=data.index)
    data["description"] = descriptionSeries
    data = data.dropna(subset=["description"])
    if typeCol and typeCol in data.columns:
        typeSeries = data[typeCol].astype(str).str.strip().str.lower()
        typeSeries = typeSeries.replace("nan", pd.NA)
        data["type"] = typeSeries.fillna("sos")
    else:
        data["type"] = "sos"
    if severityCol and severityCol in data.columns:
        severitySeries = data[severityCol].astype(str).str.strip().str.lower()
        severitySeries = severitySeries.replace("nan", pd.NA)
        data["severity"] = severitySeries.fillna("high")
    else:
        data["severity"] = "high"
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
    logger.info("Converted SOS reports to alerts format; shape=%s", result.shape)
    return result


if __name__ == "__main__":
    sample = pd.DataFrame(
        {
            "id": [101, 102, 102],
            "timestamp": [
                "2025-01-01 10:05:00",
                "2025-01-01 10:07:00",
                "2025-01-01 10:07:00",
            ],
            "lat": [26.9124, 26.9150, 26.9150],
            "lng": [75.7873, 75.7890, 75.7890],
            "message": [
                "HELP at main road!",
                " Need police at park gate  ",
                None,
            ],
        }
    )
    logger.info("Raw SOS sample:\n%s", sample)
    alertsSample = convertSosToAlerts(sample)
    logger.info("Alerts derived from SOS sample:\n%s", alertsSample)

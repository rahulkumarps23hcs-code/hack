import sys
from pathlib import Path
from typing import Any, Optional

import numpy as np
import pandas as pd

currentDir = Path(__file__).resolve().parent
utilsDir = currentDir.parent / "utils"
if str(utilsDir) not in sys.path:
    sys.path.insert(0, str(utilsDir))

from logger import getLogger
from geospatial_utils import filterInvalidCoordinates


logger = getLogger(__name__)


def loadStreetLightData(filePath: str, **readKwargs: Any) -> pd.DataFrame:
    path = Path(filePath)
    suffix = path.suffix.lower()
    if suffix == ".json":
        df = pd.read_json(path, **readKwargs)
    elif suffix == ".parquet":
        df = pd.read_parquet(path, **readKwargs)
    else:
        df = pd.read_csv(path, **readKwargs)
    logger.info("Loaded street light data from %s with shape %s", path, df.shape)
    return df


def convertLightsToSafeSpots(
    df: pd.DataFrame,
    idCol: Optional[str] = "id",
    nameCol: str = "name",
    typeCol: str = "type",
    addressCol: str = "address",
    latCol: str = "lat",
    lngCol: str = "lng",
    idPrefix: str = "S",
) -> pd.DataFrame:
    data = df.copy()
    if nameCol in data.columns:
        nameSeries = data[nameCol].fillna("").astype(str).str.strip()
    else:
        nameSeries = pd.Series("safe-spot", index=data.index)
    data["name"] = nameSeries
    if typeCol in data.columns:
        typeSeries = data[typeCol].astype(str).str.strip().str.lower()
        typeSeries = typeSeries.replace("nan", pd.NA)
        data["type"] = typeSeries.fillna("general")
    else:
        data["type"] = "general"
    if addressCol in data.columns:
        addressSeries = data[addressCol].fillna("").astype(str).str.strip()
    else:
        addressSeries = pd.Series("", index=data.index)
    data["address"] = addressSeries
    if latCol in data.columns and lngCol in data.columns:
        data = filterInvalidCoordinates(data, latCol=latCol, lngCol=lngCol)
        data = data.dropna(subset=[latCol, lngCol])
        data["lat"] = data[latCol].astype(float)
        data["lng"] = data[lngCol].astype(float)
    else:
        logger.warning(
            "Latitude/longitude columns '%s'/'%s' not found; returning empty safe spots frame.",
            latCol,
            lngCol,
        )
        return pd.DataFrame(columns=["id", "name", "type", "address", "lat", "lng"])
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
    result = data[["id", "name", "type", "address", "lat", "lng"]].reset_index(drop=True)
    logger.info("Converted street lights to safe spots format; shape=%s", result.shape)
    return result


if __name__ == "__main__":
    sample = pd.DataFrame(
        {
            "id": ["L1", "L2", "L2"],
            "name": ["Main Road Light", "Park Gate Light", None],
            "type": ["street-light", "street-light", "street-light"],
            "address": ["Main Road", "Central Park Gate", "Central Park Gate"],
            "lat": [26.9124, 26.9150, 26.9150],
            "lng": [75.7873, 75.7890, 75.7890],
        }
    )
    logger.info("Raw street light sample:\n%s", sample)
    safeSpotsSample = convertLightsToSafeSpots(sample)
    logger.info("Safe spots derived from street lights:\n%s", safeSpotsSample)

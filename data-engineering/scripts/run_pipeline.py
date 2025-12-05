"""End-to-end SAFE-ZONE data engineering pipeline.

- Optionally loads raw data from raw-data/ (if present)
- Uses cleaner scripts to convert into alert and safe-spot rows
- Delegates to dataset_merger to write alerts/safe-spots/users JSON/CSV
"""

import sys
from pathlib import Path

import pandas as pd

currentDir = Path(__file__).resolve().parent
utilsDir = currentDir.parent / "utils"
if str(utilsDir) not in sys.path:
    sys.path.insert(0, str(utilsDir))

from logger import getLogger

import crime_data_cleaner
import dataset_merger
import sos_reports_cleaner
import street_light_preprocessor


logger = getLogger(__name__)


def getBaseDir() -> Path:
    return Path(__file__).resolve().parent.parent


def getRawDir() -> Path:
    rawDir = getBaseDir() / "raw-data"
    rawDir.mkdir(parents=True, exist_ok=True)
    return rawDir


def tryLoadCsv(path: Path) -> pd.DataFrame | None:
    if not path.exists():
        logger.warning("Raw file not found: %s", path)
        return None
    df = pd.read_csv(path)
    logger.info("Loaded raw file %s with shape %s", path, df.shape)
    return df


def main() -> None:
    baseDir = getBaseDir()
    rawDir = getRawDir()

    crimeRaw = tryLoadCsv(rawDir / "crime.csv")
    sosRaw = tryLoadCsv(rawDir / "sos.csv")
    lightsRaw = tryLoadCsv(rawDir / "street-lights.csv")

    crimeAlerts = crime_data_cleaner.convertCrimeToAlerts(crimeRaw) if crimeRaw is not None else None
    sosAlerts = sos_reports_cleaner.convertSosToAlerts(sosRaw) if sosRaw is not None else None
    safeSpots = street_light_preprocessor.convertLightsToSafeSpots(lightsRaw) if lightsRaw is not None else None

    if crimeAlerts is None and sosAlerts is None:
        logger.warning("No raw crime or SOS data found; falling back to demo alerts.")
        alerts = dataset_merger.buildDemoAlerts()
    else:
        alerts = dataset_merger.buildAlertsFromFrames(crimeAlerts, sosAlerts)

    if safeSpots is None or safeSpots.empty:
        logger.warning("No raw street-light data found; falling back to demo safe spots.")
        safeSpots = dataset_merger.buildDemoSafeSpots()

    users = dataset_merger.buildDemoUsers()

    dataset_merger.writeAlertsArtifacts(alerts)
    dataset_merger.writeSafeSpotsArtifacts(safeSpots)
    dataset_merger.writeUsersArtifacts(users)

    logger.info("Pipeline finished. Check 'clean-data' for alerts/safe-spots/users.")


if __name__ == "__main__":
    main()

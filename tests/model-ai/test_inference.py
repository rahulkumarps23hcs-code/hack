import sys
from pathlib import Path

import numpy as np
import pandas as pd

projectRoot = Path(__file__).resolve().parents[2]
modelAiSrc = projectRoot / "model-ai" / "model_ai"
if str(modelAiSrc) not in sys.path:
    sys.path.insert(0, str(modelAiSrc))

from features import buildSosRiskFeatures, buildUnsafeZoneFeatures
from inference import getSosRiskScore, getUnsafeZoneScore
from sos_risk_model import saveSosRiskModel, trainSosRiskModel
from unsafe_zone_model import saveUnsafeZoneModel, trainUnsafeZoneModel


def test_training_and_inference_end_to_end(tmp_path: Path) -> None:
    alerts = pd.DataFrame(
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
                "night-time harassment report",
                "bag snatched near bus stop",
            ],
            "location.lat": [26.9124, 26.9150],
            "location.lng": [75.7873, 75.7890],
        }
    )
    from features import getCleanDataDir

    cleanDir = getCleanDataDir()
    cleanDir.mkdir(parents=True, exist_ok=True)
    alerts.to_csv(cleanDir / "alerts.csv", index=False)

    unsafeModel = trainUnsafeZoneModel()
    saveUnsafeZoneModel(unsafeModel)

    sosModel = trainSosRiskModel()
    saveSosRiskModel(sosModel)

    unsafe = getUnsafeZoneScore(26.9124, 75.7873, "2025-01-01T23:21:00Z", severity="high")
    assert 0.0 <= unsafe["unsafeScore"] <= 1.0

    risk = getSosRiskScore(
        description="help, harassment at main road",
        lat=26.9124,
        lng=75.7873,
        timestamp="2025-01-01T23:21:00Z",
        severity="high",
    )
    assert 0.0 <= risk["riskScore"] <= 1.0

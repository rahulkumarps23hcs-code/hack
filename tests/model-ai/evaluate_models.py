"""Simple evaluation script for SAFE-ZONE models.

Run after training to print metrics on the current alerts dataset.
"""

import sys
from pathlib import Path

import pandas as pd
from sklearn.metrics import classification_report

projectRoot = Path(__file__).resolve().parents[2]
modelAiSrc = projectRoot / "model-ai" / "model_ai"
if str(modelAiSrc) not in sys.path:
    sys.path.insert(0, str(modelAiSrc))

from features import buildSosRiskFeatures, buildUnsafeZoneFeatures, loadAlerts
from sos_risk_model import loadSosRiskModel
from unsafe_zone_model import loadUnsafeZoneModel


def main() -> None:
    alerts = loadAlerts()

    XUnsafe, yUnsafe = buildUnsafeZoneFeatures(alerts)
    unsafeModel = loadUnsafeZoneModel()
    yPredUnsafe = unsafeModel.predict(XUnsafe)
    print("=== Unsafe zone model metrics ===")
    print(classification_report(yUnsafe, yPredUnsafe))

    XSos, ySos = buildSosRiskFeatures(alerts)
    sosModel = loadSosRiskModel()
    yPredSos = sosModel.predict(XSos)
    print("=== SOS risk model metrics ===")
    print(classification_report(ySos, yPredSos))


if __name__ == "__main__":
    main()

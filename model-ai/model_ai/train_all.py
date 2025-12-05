from pathlib import Path

from .sos_risk_model import (
    saveSosRiskModel,
    trainSosRiskModel,
)
from .unsafe_zone_model import (
    saveUnsafeZoneModel,
    trainUnsafeZoneModel,
)


def main() -> None:
    print("Training unsafe zone model...")
    unsafeModel = trainUnsafeZoneModel()
    unsafePath = saveUnsafeZoneModel(unsafeModel)
    print(f"Saved unsafe zone model to {unsafePath}")

    print("Training SOS risk model...")
    sosModel = trainSosRiskModel()
    sosPath = saveSosRiskModel(sosModel)
    print(f"Saved SOS risk model to {sosPath}")


if __name__ == "__main__":
    main()

from __future__ import annotations

from typing import Any, Dict, List

from inference.night_mode_predictor import getMockNightModeInput, predictNightMode
from inference.safe_route_optimizer import getMockRoutesInput, optimizeSafeRoute
from inference.sos_risk_model import getMockSosRiskInput, predictSosRisk
from inference.unsafe_zone_detector import getMockUnsafeZoneInput, predictUnsafeZones
from logging_utils import logError, logInfo
from utils import buildRouteGraph


def _runImportTest() -> bool:
    try:
        _ = predictUnsafeZones  # noqa: F841
        _ = optimizeSafeRoute  # noqa: F841
        _ = predictNightMode  # noqa: F841
        _ = predictSosRisk  # noqa: F841
        return True
    except Exception as error:  # pragma: no cover
        logError("Import test failed", error)
        return False


def _runMockInferenceTest() -> bool:
    try:
        unsafeResult = predictUnsafeZones(getMockUnsafeZoneInput())
        routeResult = optimizeSafeRoute(getMockRoutesInput())
        nightResult = predictNightMode(getMockNightModeInput())
        sosResult = predictSosRisk(getMockSosRiskInput())

        _ = unsafeResult.get("alerts", [])
        _ = routeResult.get("bestRouteIndex")
        _ = nightResult.get("score")
        _ = sosResult.get("riskScore")
        return True
    except Exception as error:  # pragma: no cover
        logError("Mock inference test failed", error)
        return False


def _runRouteGraphTest() -> bool:
    try:
        routes = getMockRoutesInput()
        _ = buildRouteGraph(routes)
        return True
    except Exception as error:  # pragma: no cover
        logError("Route graph test failed", error)
        return False


def _runLoggingTest() -> bool:
    try:
        logInfo("Diagnostics logging test - info")
        logError("Diagnostics logging test - error", RuntimeError("test"))
        return True
    except Exception:  # pragma: no cover
        return False


def main() -> None:
    checks = [
        ("import", _runImportTest()),
        ("mock-inference", _runMockInferenceTest()),
        ("route-graph", _runRouteGraphTest()),
        ("logging", _runLoggingTest()),
    ]

    allOk = all(item[1] for item in checks)

    for name, status in checks:
        print(f"{name:15s}: {'OK' if status else 'FAIL'}")

    if allOk:
        print("\nAll model-ai systems OK")
    else:
        print("\nSome model-ai diagnostics failed")


if __name__ == "__main__":  # pragma: no cover
    main()

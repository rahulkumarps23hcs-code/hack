from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class UnsafeZoneConfig:
    """Configuration for unsafe zone detection and visualization."""

    probabilityThreshold: float = 0.6
    heatmapGridSize: int = 20
    # (minLat, maxLat, minLng, maxLng); if None, bounds inferred from data
    heatmapBounds: Optional[Tuple[float, float, float, float]] = None
    defaultAlertType: str = "unsafe-zone"
    defaultSeverity: str = "high"


@dataclass
class SafeRouteConfig:
    """Configuration for safe route optimization."""

    minSafeRouteScore: float = 0.5
    maxRouteLengthKm: float = 25.0


@dataclass
class NightModeConfig:
    """Configuration for smart night safety mode triggers."""

    nightStartHour: int = 22
    nightEndHour: int = 5
    triggerThreshold: float = 0.6

    # Relative weights when building the night mode score
    unsafeZoneWeight: float = 0.5
    incidentWeight: float = 0.3
    preferenceWeight: float = 0.2
    lateNightBonus: float = 0.1


@dataclass
class SosRiskConfig:
    """Configuration for SOS risk prediction."""

    highRiskThreshold: float = 0.75
    mediumRiskThreshold: float = 0.4
    triggerPromptThreshold: float = 0.6


unsafeZoneConfig = UnsafeZoneConfig()
safeRouteConfig = SafeRouteConfig()
nightModeConfig = NightModeConfig()
sosRiskConfig = SosRiskConfig()

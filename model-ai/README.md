# SAFE-ZONE AI – Model Layer

This folder contains the **model-ai** layer for the "Safe-Zone: AI-Based Women & Student Safety System".
The focus is on **modular, offline Python-only inference** with placeholder ML models.

## 1. Architecture Overview

- `config.py` – configuration dataclasses and global config instances.
- `utils.py` – geo utilities, heatmap generator, graph helpers, model singletons.
- `models/`
  - `placeholder_models.py` – simple logistic and random-forest style models.
  - `model_registry.py` – local model persistence using pickle + JSON registry.
- `inference/`
  - `unsafe_zone_detector.py` – unsafe zone prediction + heatmap + alerts.
  - `safe_route_optimizer.py` – route safety scoring using a simple graph.
  - `night_mode_predictor.py` – smart night mode activation scoring.
  - `sos_risk_model.py` – SOS risk probability and risk level.
- `preprocessing/`
  - `clean_data.py` – basic numeric cleaning and normalization.
  - `feature_engineering.py` – feature builders for the different models.
  - `validation.py` – lightweight dataclass-based schema validation helpers.
- `logging_utils.py` – simple file logger used by inference modules.
- `tests/` – unit tests for inference modules and utilities.
- `evaluation/` – scripts to run synthetic evaluations for each model.
- `adapters/` – helpers to adapt raw model outputs to backend-ready responses.
- `saved_models/` – local storage for pickled placeholder models.

## 2. Inference Flow (Conceptual)

### Unsafe Zone Detector

1. **Input**: list of location records with `location`, `recentIncidents`, `crowdScore`, etc.
2. **Feature building**: convert each record into a small feature vector.
3. **Model**: logistic-style placeholder predicts an unsafe probability.
4. **Outputs**:
   - Alert list matching the shared ALERT data model.
   - Score list with per-location probabilities and flags.
   - Heatmap description for visualization.

### Safe Route Optimizer

1. **Input**: list of candidate routes (each route is a list of `{lat, lng}` points).
2. **Graph build**: segments become edges, weighted by approximate distance.
3. **Dijkstra**: approximates a low-risk/short path over the route graph.
4. **Outputs**:
   - Best route index and route details.
   - Per-route scores and graph distances.

### Night Mode Predictor

1. **Input**: context with time, unsafe probability, incident score, user preference.
2. **Scoring**: weighted sum of risk + preference + time-of-day bonus.
3. **Output**: normalized score and a `shouldEnable` flag.

### SOS Risk Model

1. **Input**: mobility + context (speed, sudden stop, unsafe probability, time-in-app).
2. **Model**: random-forest-style placeholder over a short feature vector.
3. **Output**: risk score, risk level (low/medium/high), and whether to prompt SOS.

## 3. Config Guide

All configuration lives in `config.py`:

- `unsafeZoneConfig` – thresholds and heatmap parameters.
- `safeRouteConfig` – route length and scoring parameters.
- `nightModeConfig` – night hours, trigger thresholds, and feature weights.
- `sosRiskConfig` – thresholds for risk levels and SOS prompts.

To tune behavior, change these objects only; no code changes required.

## 4. API Contract Shapes (Model Layer)

The model layer speaks in plain Python dicts/lists that match the shared contracts:

- **Alert model**:
  ```json
  {
    "id": "...",
    "type": "...",
    "severity": "...",
    "timestamp": "...",
    "location": { "lat": 0.0, "lng": 0.0 },
    "description": "..."
  }
  ```

- **Route response** (from `safe_route_optimizer`):
  ```json
  {
    "bestRouteIndex": 0,
    "bestRoute": [ { "lat": 0.0, "lng": 0.0 }, ... ],
    "routes": [
      {
        "index": 0,
        "lengthKm": 1.23,
        "safetyScore": 0.85,
        "graphDistance": 1.23,
        "graphPath": [ [0.0, 0.0], ... ],
        "isRecommended": true
      }
    ],
    "graphUsed": true
  }
  ```

- **Night mode response**:
  ```json
  {
    "score": 0.7,
    "shouldEnable": true,
    "threshold": 0.6
  }
  ```

- **SOS risk response**:
  ```json
  {
    "riskScore": 0.8,
    "riskLevel": "high",
    "shouldPromptSos": true,
    "thresholds": {
      "high": 0.75,
      "medium": 0.4,
      "prompt": 0.6
    }
  }
  ```

These are all JSON-serializable and safe for backend APIs.

## 5. How to Test Models

From the project root:

```bash
cd model-ai
python -m unittest
```

This runs tests in `tests/`, which call the `getMock*Input()` helpers from each inference module.

To run synthetic evaluations:

```bash
cd model-ai
python evaluation/evaluate_unsafe_zone.py
python evaluation/evaluate_sos_risk.py
python evaluation/evaluate_route_safety.py
```

To run a quick full diagnostic:

```bash
cd model-ai
python run_all_diagnostics.py
```

## 6. Backend Integration Guide

Backends should treat this folder as a pure Python library layer.

Example usage from a backend service (pseudo-code):

```python
from inference.unsafe_zone_detector import predictUnsafeZones
from inference.safe_route_optimizer import optimizeSafeRoute
from inference.night_mode_predictor import predictNightMode
from inference.sos_risk_model import predictSosRisk

from adapters.backend_adapter import format_safe_response

locations = ...  # parsed request data
raw = predictUnsafeZones(locations)
response = format_safe_response(True, "ok", raw)
```

The `adapters/schema_adapter.py` module can be used to normalize outputs into the
shared ALERT / SAFE SPOT / ROUTE / RISK response shapes when needed.

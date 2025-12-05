from __future__ import annotations

import json
import os
import pickle
from datetime import datetime
from typing import Any, Dict, List


def _getBaseDirectory() -> str:
    currentDirectory = os.path.dirname(os.path.abspath(__file__))
    baseDirectory = os.path.dirname(currentDirectory)
    return baseDirectory


def _getSavedModelsDirectory() -> str:
    baseDirectory = _getBaseDirectory()
    savedDirectory = os.path.join(baseDirectory, "saved_models")
    os.makedirs(savedDirectory, exist_ok=True)
    return savedDirectory


def _getRegistryPath() -> str:
    return os.path.join(_getSavedModelsDirectory(), "registry.json")


def _loadRegistry() -> Dict[str, Any]:
    registryPath = _getRegistryPath()
    if not os.path.exists(registryPath):
        return {}
    try:
        with open(registryPath, "r", encoding="utf-8") as fileObject:
            return json.load(fileObject)
    except Exception:
        return {}


def _saveRegistry(registry: Dict[str, Any]) -> None:
    registryPath = _getRegistryPath()
    with open(registryPath, "w", encoding="utf-8") as fileObject:
        json.dump(registry, fileObject, indent=2, sort_keys=True)


def saveModel(model: Any, name: str) -> str:
    if not name:
        raise ValueError("model name must be non-empty")

    directory = _getSavedModelsDirectory()
    modelPath = os.path.join(directory, f"{name}.pkl")

    with open(modelPath, "wb") as fileObject:
        pickle.dump(model, fileObject)

    registry = _loadRegistry()
    registry[name] = {
        "name": name,
        "path": modelPath,
        "className": model.__class__.__name__,
        "savedAt": datetime.utcnow().isoformat() + "Z",
    }
    _saveRegistry(registry)

    return modelPath


def loadModel(name: str) -> Any:
    if not name:
        raise ValueError("model name must be non-empty")

    directory = _getSavedModelsDirectory()
    modelPath = os.path.join(directory, f"{name}.pkl")
    if not os.path.exists(modelPath):
        raise FileNotFoundError(f"model not found: {name}")

    with open(modelPath, "rb") as fileObject:
        model = pickle.load(fileObject)
    return model


def listModels() -> List[Dict[str, Any]]:
    registry = _loadRegistry()
    result: List[Dict[str, Any]] = []
    for item in registry.values():
        result.append(dict(item))
    return result

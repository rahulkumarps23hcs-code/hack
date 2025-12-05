from __future__ import annotations

import os
from datetime import datetime
from typing import Any, Optional


def _getLogFilePath() -> str:
    baseDirectory = os.path.dirname(os.path.abspath(__file__))
    logsDirectory = os.path.join(baseDirectory, "logs")
    os.makedirs(logsDirectory, exist_ok=True)
    return os.path.join(logsDirectory, "model.log")


def _writeLog(level: str, message: str, details: Optional[str] = None) -> None:
    timestamp = datetime.utcnow().isoformat() + "Z"
    logLine = f"{timestamp} [{level}] {message}"
    if details:
        logLine = f"{logLine} | {details}"

    logFilePath = _getLogFilePath()
    try:
        with open(logFilePath, "a", encoding="utf-8") as fileObject:
            fileObject.write(logLine + "\n")
    except Exception:
        pass


def logInfo(message: str) -> None:
    _writeLog("INFO", message)


def logWarning(message: str) -> None:
    _writeLog("WARNING", message)


def logError(message: str, error: Optional[BaseException] = None) -> None:
    details: Optional[str] = None
    if error is not None:
        details = f"{error.__class__.__name__}: {error}"
    _writeLog("ERROR", message, details=details)

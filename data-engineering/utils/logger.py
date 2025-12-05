import logging
from pathlib import Path
from typing import Optional


defaultLogFormat = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"


def getLogger(
    name: str,
    level: int = logging.INFO,
    logToFile: bool = False,
    logDir: Optional[str] = None,
    filename: Optional[str] = None,
) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        logger.setLevel(level)
        return logger
    logger.setLevel(level)
    formatter = logging.Formatter(defaultLogFormat)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)
    if logToFile:
        baseDir = Path(logDir) if logDir else Path(__file__).resolve().parent
        logsDir = baseDir / "logs"
        logsDir.mkdir(parents=True, exist_ok=True)
        fileName = filename or f"{name.replace('.', '_')}.log"
        fileHandler = logging.FileHandler(logsDir / fileName)
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)
    return logger


if __name__ == "__main__":
    demoLogger = getLogger("safeZoneDataEngineeringDemo")
    demoLogger.info("Logger initialized for SAFE-ZONE AI data engineering.")

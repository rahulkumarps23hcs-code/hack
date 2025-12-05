import sys
from typing import List

from fastapi import FastAPI, HTTPException

from config import DATABASE_NAME
from db import getDatabase
from models import (
    Alert,
    ApiResponse,
    SafeSpot,
    SosRiskRequest,
    UnsafeScoreRequest,
    User,
)

from pathlib import Path

projectRoot = Path(__file__).resolve().parents[1]
modelAiSrc = projectRoot / "model-ai" / "model_ai"
if str(modelAiSrc) not in sys.path:
    sys.path.insert(0, str(modelAiSrc))

from inference import getSosRiskScore, getUnsafeZoneScore  # type: ignore


app = FastAPI(title="SAFE-ZONE Backend", version="1.0.0")


@app.get("/alerts", response_model=ApiResponse)
async def getAlerts() -> ApiResponse:
    db = getDatabase()
    cursor = db.alerts.find({})
    alerts = [
        Alert(
            id=str(doc["id"]),
            type=doc["type"],
            severity=doc["severity"],
            timestamp=doc["timestamp"],
            location={"lat": doc["location"]["lat"], "lng": doc["location"]["lng"]},
            description=doc["description"],
        )
        for doc in cursor
    ]
    return ApiResponse(success=True, message="Alerts loaded", data=alerts)


@app.get("/safe-spots", response_model=ApiResponse)
async def getSafeSpots() -> ApiResponse:
    db = getDatabase()
    cursor = db.safespots.find({})
    spots = [
        SafeSpot(
            id=str(doc["id"]),
            name=doc["name"],
            type=doc["type"],
            address=doc["address"],
            location={"lat": doc["location"]["lat"], "lng": doc["location"]["lng"]},
        )
        for doc in cursor
    ]
    return ApiResponse(success=True, message="Safe spots loaded", data=spots)


@app.get("/users", response_model=ApiResponse)
async def getUsers() -> ApiResponse:
    db = getDatabase()
    cursor = db.users.find({})
    users = [
        User(
            id=str(doc["id"]),
            name=doc["name"],
            phone=doc["phone"],
            email=doc["email"],
        )
        for doc in cursor
    ]
    return ApiResponse(success=True, message="Users loaded", data=users)


@app.get("/unsafe-score", response_model=ApiResponse)
async def getUnsafeScoreEndpoint(request: UnsafeScoreRequest) -> ApiResponse:
    try:
        result = getUnsafeZoneScore(
            lat=request.lat,
            lng=request.lng,
            timestamp=request.timestamp,
            severity=request.severity or "medium",
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return ApiResponse(success=True, message="Unsafe score computed", data=result)


@app.post("/sos-risk", response_model=ApiResponse)
async def postSosRisk(request: SosRiskRequest) -> ApiResponse:
    try:
        result = getSosRiskScore(
            description=request.description,
            lat=request.lat,
            lng=request.lng,
            timestamp=request.timestamp,
            severity=request.severity or "high",
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return ApiResponse(success=True, message="SOS risk computed", data=result)


@app.get("/health", response_model=ApiResponse)
async def healthCheck() -> ApiResponse:
    db = getDatabase()
    collectionNames = db.list_collection_names()
    return ApiResponse(
        success=True,
        message="OK",
        data={"database": DATABASE_NAME, "collections": collectionNames},
    )

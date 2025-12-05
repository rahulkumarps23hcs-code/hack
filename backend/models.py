from typing import Any, List, Optional

from pydantic import BaseModel, Field


class Location(BaseModel):
    lat: float
    lng: float


class Alert(BaseModel):
    id: str
    type: str
    severity: str
    timestamp: str
    location: Location
    description: str


class SafeSpot(BaseModel):
    id: str
    name: str
    type: str
    address: str
    location: Location


class User(BaseModel):
    id: str
    name: str
    phone: str
    email: str


class ApiResponse(BaseModel):
    success: bool
    message: str
    data: Any


class SosRiskRequest(BaseModel):
    description: str
    lat: float
    lng: float
    timestamp: str
    severity: Optional[str] = Field(default="high")


class UnsafeScoreRequest(BaseModel):
    lat: float
    lng: float
    timestamp: str
    severity: Optional[str] = Field(default="medium")

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field(..., description="Overall system health status (healthy, degraded, unhealthy)")
    database: str = Field(..., description="Database connection status")
    database_latency_ms: Optional[float] = Field(None, description="Database ping latency in milliseconds")
    timestamp: datetime = Field(..., description="Current server UTC timestamp")
    environment: str = Field(..., description="Application execution environment")
    version: str = Field(..., description="Application software version")
    message: Optional[str] = Field(None, description="Additional context or diagnostics")

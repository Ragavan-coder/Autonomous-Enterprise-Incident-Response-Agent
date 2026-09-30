from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
from datetime import datetime

class IncidentState(str, Enum):
    CREATED = "CREATED"
    TRIAGING = "TRIAGING"
    INVESTIGATING = "INVESTIGATING"
    ROOT_CAUSE_ANALYSIS = "ROOT_CAUSE_ANALYSIS"
    AWAITING_APPROVAL = "AWAITING_APPROVAL"
    REMEDIATING = "REMEDIATING"
    VERIFYING = "VERIFYING"
    RESOLVED = "RESOLVED"
    FAILED = "FAILED"
    CLOSED = "CLOSED"

class Severity(str, Enum):
    SEV1 = "SEV1"
    SEV2 = "SEV2"
    SEV3 = "SEV3"
    SEV4 = "SEV4"

class IncidentCreate(BaseModel):
    title: str
    description: str
    service: str
    severity: Severity

class Incident(IncidentCreate):
    id: str
    status: IncidentState
    created_at: datetime
    updated_at: datetime
    investigation_duration: Optional[float] = None
    affected_services: List[str] = []

class IncidentEvent(BaseModel):
    id: str
    incident_id: str
    timestamp: datetime
    actor: str
    event: str
    details: str

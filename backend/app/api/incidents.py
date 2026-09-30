from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from datetime import datetime
import uuid
from app.models.incident import IncidentCreate, Incident, IncidentState
from app.agents.incident_manager import trigger_investigation

router = APIRouter()

# In-memory store for simulation purposes
# In a real app, this would use Postgres via app.database
incidents_db: Dict[str, Incident] = {}
traces_db: Dict[str, List[Dict[str, Any]]] = {}

@router.post("/", response_model=Incident)
def create_incident(incident: IncidentCreate):
    inc_id = f"inc-{uuid.uuid4().hex[:8]}"
    new_incident = Incident(
        id=inc_id,
        title=incident.title,
        description=incident.description,
        service=incident.service,
        severity=incident.severity,
        status=IncidentState.CREATED,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    incidents_db[inc_id] = new_incident
    return new_incident

@router.get("/", response_model=List[Incident])
def list_incidents():
    return list(incidents_db.values())

@router.get("/{id}", response_model=Incident)
def get_incident(id: str):
    if id not in incidents_db:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incidents_db[id]

@router.post("/{id}/investigate")
def investigate_incident(id: str):
    if id not in incidents_db:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    incident = incidents_db[id]
    incident.status = IncidentState.INVESTIGATING
    incident.updated_at = datetime.utcnow()
    
    # Trigger background agent investigation
    # For demo purposes we can run it synchronously or queue it
    trace = trigger_investigation(incident.dict())
    traces_db[id] = trace
    
    # If the investigation led to an approval requirement
    incident.status = IncidentState.AWAITING_APPROVAL
    incident.updated_at = datetime.utcnow()
    
    return {"status": "investigation_completed", "incident": incident}

@router.get("/{id}/trace")
def get_trace(id: str):
    if id not in traces_db:
        raise HTTPException(status_code=404, detail="Trace not found")
    return {"trace": traces_db[id]}

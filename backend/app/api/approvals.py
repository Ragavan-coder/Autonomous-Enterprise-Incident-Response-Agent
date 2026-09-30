from fastapi import APIRouter

router = APIRouter()

@router.post("/{incident_id}/approve")
def approve_action(incident_id: str):
    from app.api.incidents import incidents_db
    from app.models.incident import IncidentState
    if incident_id in incidents_db:
        incidents_db[incident_id].status = IncidentState.REMEDIATING
    return {"status": "approved"}

@router.post("/{incident_id}/reject")
def reject_action(incident_id: str):
    from app.api.incidents import incidents_db
    from app.models.incident import IncidentState
    if incident_id in incidents_db:
        incidents_db[incident_id].status = IncidentState.FAILED
    return {"status": "rejected"}

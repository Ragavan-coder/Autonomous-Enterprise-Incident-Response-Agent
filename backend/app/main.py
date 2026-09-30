from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import incidents, services, evaluations, approvals
from app.database.connection import initialize_database

app = FastAPI(title="Autonomous Enterprise Incident Response Agent (AIRA)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    # initialize_database()
    pass

app.include_router(incidents.router, prefix="/api/incidents", tags=["Incidents"])
app.include_router(services.router, prefix="/api/services", tags=["Services"])
app.include_router(evaluations.router, prefix="/api/evaluations", tags=["Evaluations"])
app.include_router(approvals.router, prefix="/api/approvals", tags=["Approvals"])

@app.get("/health")
def health_check():
    return {"status": "ok"}

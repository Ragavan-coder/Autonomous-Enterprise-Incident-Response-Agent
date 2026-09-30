from pydantic import BaseModel
from typing import List, Optional

class Evidence(BaseModel):
    source: str
    reference: str
    details: str

class AlternativeHypothesis(BaseModel):
    hypothesis: str
    confidence: float

class RootCauseAnalysis(BaseModel):
    root_cause: str
    confidence: float
    evidence: List[Evidence]
    alternatives: List[AlternativeHypothesis]

class RemediationProposal(BaseModel):
    action: str
    risk: str  # HIGH, MEDIUM, LOW
    reason: str
    rollback_available: bool
    rollback_strategy: str
    verification_criteria: str

class VerificationResult(BaseModel):
    passed: bool
    details: str
    metrics_before: dict
    metrics_after: dict

class Postmortem(BaseModel):
    incident_id: str
    summary: str
    impact: str
    timeline: List[str]
    detection: str
    root_cause: str
    evidence: List[Evidence]
    contributing_factors: List[str]
    remediation: str
    verification: str
    prevention: str
    related_runbooks: List[str]
    related_incidents: List[str]

from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/")
def list_evaluations():
    return {"evaluations": []}

@router.post("/run")
def run_evaluation():
    # Trigger evaluation suite
    return {"status": "started"}

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict
import uuid
import asyncio
import random

app = FastAPI(title="GenAI Platform Fine-Tuning Service")

# --- Models ---
class TrainingJobCreate(BaseModel):
    tenant_id: str
    base_model: str # e.g., "llama-2-7b"
    dataset_url: str
    epochs: int = 3

class TrainingJobStatus(BaseModel):
    id: str
    status: str # pending, running, completed, failed
    progress: float # 0.0 to 1.0
    metrics: Dict[str, float] = {}

# --- Mock Database ---
jobs_db: Dict[str, dict] = {}

# --- Background Task ---
async def run_training_job_mock(job_id: str, epochs: int):
    jobs_db[job_id]["status"] = "running"
    
    for epoch in range(1, epochs + 1):
        # Simulate training time per epoch
        await asyncio.sleep(2) 
        
        # Update progress
        jobs_db[job_id]["progress"] = epoch / epochs
        
        # Mock metrics (decreasing loss)
        current_loss = 2.5 - (2.0 * (epoch / epochs)) + (random.random() * 0.1)
        jobs_db[job_id]["metrics"] = {"loss": round(current_loss, 4), "epoch": epoch}
        
    jobs_db[job_id]["status"] = "completed"
    jobs_db[job_id]["metrics"]["final_loss"] = jobs_db[job_id]["metrics"]["loss"]

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "fine-tuning"}

@app.post("/jobs", response_model=TrainingJobStatus)
async def create_training_job(job_in: TrainingJobCreate, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    
    # Init job state
    job_state = {
        "id": job_id,
        "status": "pending",
        "progress": 0.0,
        "metrics": {},
        "tenant_id": job_in.tenant_id,
        "base_model": job_in.base_model
    }
    jobs_db[job_id] = job_state
    
    # Start background task
    background_tasks.add_task(run_training_job_mock, job_id, job_in.epochs)
    
    return TrainingJobStatus(**job_state)

@app.get("/jobs/{job_id}", response_model=TrainingJobStatus)
async def get_job_status(job_id: str):
    if job_id not in jobs_db:
        raise HTTPException(status_code=404, detail="Job not found")
    return TrainingJobStatus(**jobs_db[job_id])

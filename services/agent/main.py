from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uuid
import asyncio

app = FastAPI(title="GenAI Platform Agent Service")

# --- Models ---
class AgentCreate(BaseModel):
    tenant_id: str
    name: str
    description: str
    tools: List[str] # e.g. ["rag", "web_search", "calculator"]
    system_prompt: str

class AgentExecutionRequest(BaseModel):
    tenant_id: str
    agent_id: str
    input: str

class ExecutionResult(BaseModel):
    status: str
    result: str
    steps: List[str]

# --- Mock Storage ---
agents_db = {}

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "agent"}

@app.post("/agents")
async def create_agent(agent_in: AgentCreate):
    agent_id = str(uuid.uuid4())
    agents_db[agent_id] = agent_in
    return {"id": agent_id, "status": "created"}

@app.post("/execute", response_model=ExecutionResult)
async def execute_agent(req: AgentExecutionRequest):
    if req.agent_id not in agents_db:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    agent = agents_db[req.agent_id]
    
    # Verify Tenant Ownership (Mock)
    if agent.tenant_id != req.tenant_id:
        raise HTTPException(status_code=403, detail="Unauthorized access to this agent")

    # Simulate detailed agent execution loop
    steps = []
    
    # Step 1: Planning
    steps.append(f"Agent '{agent.name}' received input: '{req.input}'")
    steps.append("Thinking: Decomposing task...")
    
    # Step 2: Tool Usage (Simulation)
    result_text = "Analysis complete."
    if "rag" in agent.tools:
        steps.append("Action: calling RAG service for context...")
        # In real world, would HTTP call the RAG service here
        steps.append("Observation: Found relevant documents regarding query.")
        result_text += " Based on internal knowledge base, here is the answer."
        
    if "web_search" in agent.tools:
        steps.append("Action: Searching web for latest info...")
        steps.append("Observation: Retrieved top 3 results.")
        result_text += " Supplemented with live web data."

    if "calculator" in agent.tools:
        steps.append("Action: Calculating metrics...")
        steps.append("Observation: Result is 42.")
    
    # Step 3: Synthesis
    steps.append("Final Answer: Generated response.")
    
    # Simulate processing time
    await asyncio.sleep(0.5)
    
    return ExecutionResult(
        status="completed",
        result=f"Processed '{req.input}' via agent '{agent.name}'. {result_text}",
        steps=steps
    )

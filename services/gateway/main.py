from fastapi import FastAPI, Request, HTTPException
import httpx
import os

app = FastAPI(title="GenAI Platform Gateway")

# Service URLs from env or default to docker-compose names
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://genai_auth:8000")
RAG_SERVICE_URL = os.getenv("RAG_SERVICE_URL", "http://genai_rag:8000")

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "gateway"}

# --- Audit Logging Middleware ---
@app.middleware("http")
async def audit_logging_middleware(request: Request, call_next):
    # Extract tenant info if available (mock logic)
    tenant_id = request.headers.get("x-tenant-id", "anonymous")
    
    # Process request
    response = await call_next(request)
    
    # Log structured data
    log_entry = {
        "event": "api_request",
        "method": request.method,
        "path": request.url.path,
        "tenant_id": tenant_id,
        "status_code": response.status_code
    }
    print(f"AUDIT_LOG: {log_entry}") # In real app, send to file or logging service
    
    return response

@app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy(path_name: str, request: Request):
    # Simple proxy logic (will be refined later)
    # Determine target service based on path prefix
    
    target_url = None
    if path_name.startswith("auth"):
        target_url = f"{AUTH_SERVICE_URL}/{path_name}"
    elif path_name.startswith("rag"):
        target_url = f"{RAG_SERVICE_URL}/{path_name}"
    
    if not target_url:
        return {"message": "Service not found or path not routed"}

    async with httpx.AsyncClient() as client:
        try:
            # Forwarding request
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=request.headers,
                content=await request.body()
            )
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Service Unavailable: {str(e)}")

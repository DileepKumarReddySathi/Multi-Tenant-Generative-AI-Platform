from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import uuid
import os

app = FastAPI(title="GenAI Platform Billing Service")

# --- Models ---
class CheckoutRequest(BaseModel):
    tenant_id: str
    plan_id: str # e.g., "price_premium_monthly"

class PortalRequest(BaseModel):
    tenant_id: str

# --- Mock Data ---
subscriptions_db = {} # tenant_id -> subscription_status

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "billing"}

@app.post("/create-checkout-session")
async def create_checkout_session(req: CheckoutRequest):
    # Simulate Stripe Checkout Session creation
    session_id = f"cs_test_{str(uuid.uuid4())}"
    checkout_url = f"https://checkout.stripe.mock/pay/{session_id}?prefilled_email=tenant@example.com"
    
    # In a real app, we don't activate until webhook, but for mock immediate gratification:
    subscriptions_db[req.tenant_id] = "active" 
    
    return {
        "sessionId": session_id,
        "url": checkout_url
    }

@app.post("/create-portal-session")
async def create_portal_session(req: PortalRequest):
    # Simulate Stripe Customer Portal
    return {
        "url": "https://billing.stripe.mock/p/session/test_12345"
    }

@app.post("/webhook")
async def stripe_webhook(request: Request):
    # Mock webhook handler
    payload = await request.json()
    event_type = payload.get("type")
    
    if event_type == "checkout.session.completed":
        # Handle successful payment
        data = payload.get("data", {}).get("object", {})
        tenant_id = data.get("client_reference_id")
        if tenant_id:
            subscriptions_db[tenant_id] = "active"
            print(f"Activated subscription for tenant {tenant_id}")
            
    return {"status": "received"}

@app.get("/subscription/{tenant_id}")
async def get_subscription_status(tenant_id: str):
    return {"status": subscriptions_db.get(tenant_id, "free")}

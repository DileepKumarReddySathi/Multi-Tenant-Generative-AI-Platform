from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List, Optional
import uuid

app = FastAPI(title="GenAI Platform Auth Service")

# --- Models ---
class Tenant(BaseModel):
    id: str
    name: str
    plan: str = "free"

class User(BaseModel):
    id: str
    email: str
    full_name: str
    tenant_id: str
    role: str = "user" # admin, user

class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str
    tenant_name: str # For simplicity, create tenant on signup

class Token(BaseModel):
    access_token: str
    token_type: str

# --- Mock Database ---
# In a real app, use SQLAlchemy/SQLModel with Postgres
users_db = {}
tenants_db = {}

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "auth"}

@app.post("/register", response_model=User)
async def register(user_in: UserCreate):
    # Check if user exists
    for u in users_db.values():
        if u.email == user_in.email:
            raise HTTPException(status_code=400, detail="Email already registered")

    # Create Tenant
    tenant_id = str(uuid.uuid4())
    tenant = Tenant(id=tenant_id, name=user_in.tenant_name)
    tenants_db[tenant_id] = tenant

    # Create User
    user_id = str(uuid.uuid4())
    user = User(
        id=user_id,
        email=user_in.email,
        full_name=user_in.full_name,
        tenant_id=tenant_id,
        role="admin" # First user is admin
    )
    users_db[user_id] = user
    
    # TODO: Hash password and store auth credential
    
    return user

@app.post("/token", response_model=Token)
async def login(form_data: UserCreate): # Using UserCreate for simplicity here, normally OAuth2PasswordRequestForm
    # Verify mock credentials
    user = None
    for u in users_db.values():
        if u.email == form_data.email:
             # Check password (mock)
            user = u
            break
            
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
        
    # Generate JWT (mock)
    return {"access_token": f"fake-jwt-token-for-{user.id}", "token_type": "bearer"}

@app.get("/users/me", response_model=User)
async def read_users_me(token: str):
    # Parse mock token
    # In real app, verify JWT signature and decode
    try:
        user_id = token.split("-")[-1]
        if user_id in users_db:
             return users_db[user_id]
    except:
        pass
    raise HTTPException(status_code=401, detail="Invalid token")

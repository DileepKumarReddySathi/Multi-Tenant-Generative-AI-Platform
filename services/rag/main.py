from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import os
import asyncpg
import json
# In a real app, use langchain or llama-index for chunking/embedding
# Here we will mock embeddings for simplicity to demonstrate the architecture

app = FastAPI(title="GenAI Platform RAG Service")

DB_DSN = os.getenv("DATABASE_URL", "postgresql://admin:password@postgres:5432/genai_platform")

# --- Models ---
class DocumentIngest(BaseModel):
    tenant_id: str
    content: str
    metadata: dict = {}

class QueryRequest(BaseModel):
    tenant_id: str
    query: str
    k: int = 3

class SearchResult(BaseModel):
    content: str
    score: float
    metadata: dict

# --- Database Utils ---
async def get_db_connection():
    return await asyncpg.connect(DB_DSN)

async def init_db():
    conn = await get_db_connection()
    try:
        # Enable pgvector extension
        await conn.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        # Create table with separate fields for tenant isolation
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS embeddings (
                id SERIAL PRIMARY KEY,
                tenant_id VARCHAR(255) NOT NULL,
                content TEXT NOT NULL,
                metadata JSONB,
                embedding vector(3) -- Mock 3-dim vector for simple demo
            );
        """)
    finally:
        await conn.close()

# --- Mock Embedding Function ---
def mock_embed(text: str) -> List[float]:
    # Deterministic mock embedding based on text length
    val = len(text) % 10 / 10.0
    return [val, val, val]

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "rag"}

@app.post("/ingest")
async def ingest_document(doc: DocumentIngest):
    conn = await get_db_connection()
    try:
        embedding = mock_embed(doc.content)
        embedding_str = f"[{','.join(map(str, embedding))}]"
        
        await conn.execute(
            """
            INSERT INTO embeddings (tenant_id, content, metadata, embedding)
            VALUES ($1, $2, $3, $4)
            """,
            doc.tenant_id, doc.content, json.dumps(doc.metadata), embedding_str
        )
        return {"status": "ingested", "chunks": 1}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await conn.close()

@app.post("/query", response_model=List[SearchResult])
async def search_vectors(query: QueryRequest):
    conn = await get_db_connection()
    try:
        query_vec = mock_embed(query.query)
        query_vec_str = f"[{','.join(map(str, query_vec))}]"
        
        # Simple RLS-like filter: WHERE tenant_id = $1
        rows = await conn.fetch(
            """
            SELECT content, metadata, 1 - (embedding <=> $2) as score
            FROM embeddings
            WHERE tenant_id = $1
            ORDER BY embedding <=> $2
            LIMIT $3
            """,
            query.tenant_id, query_vec_str, query.k
        )
        
        results = []
        for row in rows:
            results.append(SearchResult(
                content=row['content'],
                score=row['score'],
                metadata=json.loads(row['metadata'])
            ))
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await conn.close()

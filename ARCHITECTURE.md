# System Architecture - Multi-Tenant GenAI Platform

## 1. High-Level Overview

The platform uses a microservices architecture to provide scalable, isolated, and secure Generative AI capabilities to multiple tenants. Services are containerized using Docker and orchestrated via Docker Compose (support for K8s implied).

### Core Components
- **API Gateway**: Single entry point handling routing, rate limiting, and initial request logging.
- **Auth Service**: Centralized identity provider issuing JWTs with tenant context (RBAC).
- **Billing Service**: Manages subscriptions and mock Stripe integration.
- **Frontend**: Next.js application serving both Admin (Superuser) and Tenant (User) portals.

### AI Microservices
- **RAG Service**: Handles document ingestion, chunking, embedding generation, and vector retrieval using PostgreSQL (`pgvector`).
- **Agent Service**: Orchestrates AI agents using LangChain primitives (mocked), executing multi-step reasoning tasks.
- **Multimodal Service**: Interfaces with image generation/analysis models.
- **Fine-Tuning Service**: Manages long-running training jobs using an async task queue pattern.

## 2. Data Isolation Strategy

Strict data isolation is enforced at the Application and Database layers.

### Database Isolation
- **Pattern**: **Shared Database, Shared Schema**, with **Row-Level Security (RLS)** logic.
- **Implementation**:
    - Every table (e.g., `users`, `embeddings`, `jobs`) includes a `tenant_id` column.
    - All service queries **MUST** include `WHERE tenant_id = <request_tenant_id>`.
    - The `pgvector` store separates vector indices logically by filtering on `tenant_id` during similarity search.

### Storage Isolation
- **Object Storage (MinIO)**:
    - Files are stored in paths structured as `{tenant_id}/{document_id}`.
    - Access policies restrict tenants to their specific prefix.

## 3. Security Architecture

### Authentication & Authorization
- **Auth Flow**: Users authenticate via the Auth Service to receive a JWT.
- **Token Structure**: JWT contains standard claims (`sub`, `exp`) and custom claims (`tenant_id`, `role`).
- **Service-to-Service**: Internal services trust the JWT passed by the Gateway/Auth service.

### Network Security
- **API Gateway**: Acts as the reverse proxy. Internal microservices are not exposed directly to the public internet (internal Docker network `genai_net`).

## 4. Observability

- **Metrics**: Services expose prometheus-compatible metrics (mocked endpoint).
- **Logging**: The Gateway implements an Audit Logging middleware that captures structured logs (`event`, `tenant_id`, `path`) for every request, ensuring full traceability of tenant actions.

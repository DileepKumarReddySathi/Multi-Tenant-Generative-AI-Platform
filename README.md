# Multi-Tenant Generative AI Platform

A production-grade, multi-tenant platform for Generative AI applications using RAG, Agents, and Fine-tuning.

## Tech Stack

- **Frontend**: Next.js 14, React, TailwindCSS, Shadcn/UI
- **Backend**: Python, FastAPI
- **Database**: PostgreSQL (pgvector)
- **Infrastructure**: Docker, Redis, MinIO
- **Observability**: Prometheus, Grafana

## Documentation

- [Architecture Overview](ARCHITECTURE.md) - Deep dive into system design and security.
- [Walkthrough](walkthrough.md) - Step-by-step guide.
- [Submission Config](submission.yml) - Automated testing configuration.

## Getting Started

### Prerequisites
- Docker & Docker Compose
- Node.js (v20+)

### 1. Start Infrastructure & Microservices

Run the following command in the project root to build and start all services:

```bash
docker-compose up -d --build
```

Wait a few moments for all containers to be healthy.

### 2. Start Frontend Application

Navigate to the web app directory and start the dev server:

```bash
cd apps/web
npm run dev
```

The application will be available at [http://localhost:3000](http://localhost:3000).

## Verification & Usage

### 1. Admin Portal
- URL: [http://localhost:3000/admin](http://localhost:3000/admin)
- Features: View tenant metrics, system health, and billing stats.

### 2. Tenant Portal
- URL: [http://localhost:3000/tenant](http://localhost:3000/tenant)
- Features:
    - **Dashboard**: View API usage and vector storage stats.
    - **AI Chat**: Interact with the RAG service (mocked response).
    - **Agent Builder**: Create and manage AI agents.

### 3. Service Endpoints (API)

| Service | Port | Endpoint | Description |
| :--- | :--- | :--- | :--- |
| **Gateway** | 8000 | `/` | Main API Gateway |
| **Auth** | 8001 | `/health` | Identity & Tenants |
| **RAG** | 8002 | `/ingest` | Vector DB & Retrieval |
| **Agent** | 8003 | `/execute` | Agent Orchestration |
| **Multimodal** | 8004 | `/generate` | Image Gen/Analysis |
| **Billing** | 8005 | `/checkout` | Stripe Mock |
| **Fine-Tuning** | 8006 | `/jobs` | Training Jobs |

### 4. Observability

- **Prometheus**: [http://localhost:9090](http://localhost:9090) - Metrics scraping.
- **Grafana**: [http://localhost:3001](http://localhost:3001) - Dashboards (Login: admin/admin).

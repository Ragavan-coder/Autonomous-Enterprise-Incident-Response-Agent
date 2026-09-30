# Autonomous Enterprise Incident Response Agent (AIRA)

## Project Overview
AIRA is a full-stack, AI-driven platform for investigating and remediating production incidents autonomously. 
It uses Generative AI, Tool Calling, and multi-agent orchestration to investigate issues within a simulated microservice architecture.

## Problem Statement
Traditional incident response is manual, slow, and error-prone. This project demonstrates how agentic AI can automate the investigation of logs, metrics, service graphs, and deployments to identify root causes and propose remediations.

## Architecture
- **Frontend**: Next.js (TypeScript) dashboard for observability.
- **Backend**: FastAPI (Python) driving the AI Agents.
- **Data**: PostgreSQL with pgvector for RAG, Redis for caching.
- **AI**: OpenAI models with function calling for agent orchestration.
- **Graph Engine**: BFS/DFS/Dijkstra for dependency analysis.

## Agent Architecture
- **Incident Manager**: Coordinates the triage.
- **Investigation Agent**: Calls tools (metrics, logs).
- **Root Cause Agent**: Evaluates evidence and generates hypotheses.
- **Remediation Agent**: Proposes safe actions subject to human approval.



## Security & Guardrails
- **Prompt Injection Defense**: Untrusted text from RAG or logs cannot execute arbitrary tools.
- **Human Approval**: High-risk actions (e.g., Rollback) pause the agent until human approval is received.
- **Tool Policies**: Tools are scoped and restricted based on simulated RBAC.

## Database
Uses PostgreSQL schemas for `incidents`, `events`, `documents`, `audit_logs`, and vector embeddings.

## Note
This is a simulation platform. It does NOT connect to real infrastructure.

# Autonomous-Enterprise-Incident-Response-Agent

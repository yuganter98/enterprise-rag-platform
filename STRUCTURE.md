# Project Folder Structure & Responsibilities

This document outlines the organization of the Enterprise AI Assistant backend. The structure follows a **Domain-Driven Design (DDD)** approach to ensure scalability, maintainability, and clear separation of concerns.

## root/
- **`app/`**: The core application logic.
- **`alembic/`**: Database migration scripts (version control for your DB schema).
- **`tests/`**: Automated tests (using `pytest`).
- **`data/`**: Local storage for raw documents (e.g., PDF uploads) before processing. **(Gitignored)**
- **`docs/`**: Project documentation and architecture diagrams.
- **`scripts/`**: Utility scripts for devops, setup, or maintenance.
- **`.env`**: Environment variables (secrets, API keys, DB URL). **(Gitignored)**

## app/
The heart of the application.

### `api/`
Handles HTTP requests and responses.
- **`v1/`**: API Versioning (future-proofing).
- **`v1/endpoints/`**: Individual route modules (e.g., `auth.py`, `employees.py`, `chat.py`).
- **`deps.py`**: **Dependencies**. Reusable logic injected into routes (e.g., `get_current_user`, `get_db_session`). This is a key FastAPI feature.

### `core/`
Global configurations and low-level core modifications.
- **`config.py`**: Settings management using Pydantic (loads env vars).
- **`security.py`**: JWT token creation/validation, password hashing.
- **`exceptions.py`**: Custom exception classes and handlers.

### `db/`
Database connectivity and initialization.
- **`session.py`**: Configures the SQLAlchemy engine and session factory.
- **`base.py`**: Imports all models so Alembic can find them for migration generation.
- **`init_db.py`**: Script to seed the database with initial data (e.g., admin user).

### `models/`
**SQLAlchemy ORM Models.**
- Represents database tables (e.g., `User`, `Employee`, `Document`).
- Defines relationships and constraints.

### `schemas/`
**Pydantic Models (DTOs - Data Transfer Objects).**
- Defines the shape of data entering (Request) and leaving (Response) the API.
- Handles data validation automatically.
- Keeps internal DB models separate from public API contracts.

### `services/`
**Business Logic Layer.**
- Contains the complex logic, decoupled from the API routes.
- **`rag/`**: Logic for Ingestion (parsing PDFs), Retrieval (vector search), and Generation (LLM calls).
- **`email/`**: Logic for formatting and sending emails.
- **`report/`**: Logic for processing data and generating Excel files.
- **`auth_service.py`**: High-level authentication flows.

### `utils/`
General utility functions (e.g., date formatting, string helpers).

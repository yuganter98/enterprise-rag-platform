# Enterprise AI RAG Platform

> A secure, enterprise-grade AI Assistant capable of context-aware Chat (RAG) on proprietary documents, Event Management, and Role-Based Access Control (RBAC).

[![CI](https://github.com/yuganter98/enterprise-rag-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/yuganter98/enterprise-rag-platform/actions/workflows/ci.yml)

## 🚀 Project Overview

The **Enterprise AI RAG Platform** is designed to solve the challenge of securely deploying Large Language Models (LLMs) within an organization. Unlike public chatbots, this system allows employees to query **internal documents** (PDFs, Text) without data leaving the secure environment.

It features a rigorous **Role-Based Access Control (RBAC)** system, ensuring that only Administrators can manage users, view sensitive reports, or modify system configurations, while standard Employees have restricted "View-Only" and "Event" access.

### Key Features

*   **🤖 Intelligent Document Chat (RAG)**
    *   **Retrieval-Augmented Generation**: Upload proprietary PDFs and text documents.
    *   **Context-Aware**: The AI cites specific sources from your uploaded knowledge base.
    *   **Local LLM Ready**: Compatible with LM Studio for fully offline/private inference.

*   **🛡️ Role-Based Security (RBAC)**
    *   **Admin**: Full access (User Management, Document Uploads, Reports, System Config).
    *   **Employee**: Restricted access (Events Calendar, Chat - pending config).
    *   **Secure Auth**: JWT-based stateless authentication.

*   **📅 Event Management System**
    *   **Admin Scheduling**: Create and manage company-wide events.
    *   **Automated Notifications**: Automatically sends SMTP email alerts to all employees upon event creation.
    *   **Interactive Calendar**: Visual dashboard for upcoming activities.

*   **📊 Reporting & Analytics**
    *   **Excel Exports**: Generate and download detailed .xlsx reports of system usage and logs.

## 🛠️ Technology Stack

**Frontend**
*   **Framework**: React 18 (Vite)
*   **Language**: TypeScript
*   **Styling**: Tailwind CSS + Lucide React (Glassmorphism Design)
*   **State**: Context API

**Backend**
*   **Framework**: FastAPI (Python 3.11+)
*   **Database**: SQLite (Dev) / PostgreSQL (Prod) with SQLAlchemy ORM
*   **Migrations**: Alembic
*   **AI/ML**: LangChain, FAISS (Vector Store)

---

## 🐳 Quick Start (Docker)

Runs Postgres (with pgvector), the API and the frontend with one command.

```bash
git clone https://github.com/yuganter98/enterprise-rag-platform.git
cd enterprise-rag-platform
cp .env.example .env          # set FIRST_SUPERUSER_PASSWORD (and SECRET_KEY)
docker compose up --build
```

*   Frontend: `http://localhost:5173`
*   API docs (Swagger): `http://localhost:8000/docs`

The API container applies migrations and creates the admin account on start. To load the demo company data (users, events and sample documents with role-based visibility):

```bash
docker compose exec api python scripts/seed_demo.py
```

For chat answers, run [LM Studio](https://lmstudio.ai/) on your machine with its local server on port 1234; the container reaches it via `host.docker.internal`.

## 🎭 Demo Data

`scripts/seed_demo.py` loads a fictional company, *Lumen Dynamics*, from [`sample_docs/`](sample_docs):

| Document | Visible to |
|---|---|
| `employee_handbook.txt` (leave, remote work, expenses) | admin, hr, employee |
| `it_security_policy.txt` (passwords, MFA, devices) | admin, hr, employee |
| `hr_compensation_guidelines.txt` (salary bands, bonuses) | admin, hr |
| `board_strategy_2027.txt` (expansion plans, revenue targets) | admin |

Demo logins: `employee@lumen.example` and `hr@lumen.example`, with the password from `DEMO_USER_PASSWORD` (development default: `demo-password-123`). Ask each one about salary bands to see role-based retrieval in action.

## 💻 Manual Setup

### Prerequisites
*   Python 3.11+
*   Node.js 20+ and [pnpm](https://pnpm.io/)
*   (Optional) [LM Studio](https://lmstudio.ai/) running locally for AI inference.

### 1. Backend Setup

```bash
# Navigate to project root
cd enterprise-rag-platform

# Create a virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env: set SECRET_KEY, FIRST_SUPERUSER_PASSWORD and SMTP settings.
# Generate a key with: python -c "import secrets; print(secrets.token_urlsafe(48))"

# Initialize Database and create the admin account
alembic upgrade head
python -m app.initial_data

# Run the Server
python -m uvicorn app.main:app --reload
```
The Backend API will run at `http://localhost:8000`.

### 2. Frontend Setup

```bash
# Open a new terminal and navigate to frontend
cd frontend

# Install dependencies
pnpm install

# Run the Development Server
pnpm dev
```
The Frontend UI will run at `http://localhost:5173`. Set `VITE_API_URL` to point it at a different API.

## ✅ Testing

```bash
pip install -r requirements-dev.txt
pytest          # API, RBAC, uploads, retrieval, chat, email, reports, config
ruff check .    # lint
```

The tests use a throwaway SQLite database and a fake embedding model, so they need no GPU, model download or LLM. GitHub Actions runs them on every push and pull request, along with Alembic migrations against Postgres, a frontend build, and a Docker Compose smoke test.

---

## 🔐 Security Configuration

*   `ENVIRONMENT=production` makes the API refuse to start if `SECRET_KEY` is missing or shorter than 32 characters, or if the admin/database passwords are still the development defaults.
*   In development, missing values only produce warnings, and a random `SECRET_KEY` is generated on each start (so you'll need to log in again after a restart). Set `SECRET_KEY` in `.env` to avoid that.
*   Uploads are admin-only, limited to `MAX_UPLOAD_SIZE_MB` (default 20) and the allowed file types, and are stored under random names.

## 📖 Usage Guide

1.  **Login**: Access the dashboard at `http://localhost:5173`.
    *   *Admin account*: `FIRST_SUPERUSER` / `FIRST_SUPERUSER_PASSWORD` from your `.env`.
2.  **Upload Documents**: Go to the **Documents** tab (Admin only) to upload PDF, TXT, DOCX, CSV or XLSX files and choose which roles can see them.
3.  **Chat**: Use the **Chat** interface to query your uploaded documents.
4.  **Manage Users**: Go to **Users** (Admin only) to create new Employee accounts.
5.  **Events**: Check the **Events** tab to see company schedules.

## 🤝 Contributing

1.  Fork the repository.
2.  Create a feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

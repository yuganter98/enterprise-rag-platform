# Enterprise AI RAG Platform

> A secure, enterprise-grade AI Assistant capable of context-aware Chat (RAG) on proprietary documents, Event Management, and Role-Based Access Control (RBAC).

![Enterprise AI Dashboard](https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=2070&auto=format&fit=crop)

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
*   **Framework**: FastAPI (Python 3.10+)
*   **Database**: SQLite (Dev) / PostgreSQL (Prod) with SQLAlchemy ORM
*   **Migrations**: Alembic
*   **AI/ML**: LangChain, FAISS (Vector Store)

---

## 💻 Installation & Setup Guide

Follow these steps to run the application locally.

### Prerequisites
*   Python 3.10+
*   Node.js 18+
*   (Optional) [LM Studio](https://lmstudio.ai/) running locally for AI inference.

### 1. Backend Setup

```bash
# Navigate to project root
cd enterprise-ai-assistant

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
# (Edit .env with your secret keys and SMTP settings)

# Initialize Database
alembic upgrade head

# Run the Server
python -m uvicorn app.main:app --reload
```
The Backend API will run at `http://localhost:8000`.

### 2. Frontend Setup

```bash
# Open a new terminal and navigate to frontend
cd frontend

# Install dependencies
npm install

# Run the Development Server
npm run dev
```
The Frontend UI will run at `http://localhost:5173`.

---

## 📖 Usage Guide

1.  **Login**: Access the dashboard at `http://localhost:5173`.
    *   *Default Admin*: (Check `app/initial_data.py` or create your own via API/Swagger).
2.  **Upload Documents**: Go to the **Documents** tab (Admin only) to upload PDFs.
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

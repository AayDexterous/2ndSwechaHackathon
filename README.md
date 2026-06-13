# QuickPic (Simple Social)

A fast, lightweight social sharing application featuring a FastAPI backend, a Streamlit frontend, secure JWT authentication, and dynamic media transformations powered by ImageKit.io.

---

## Table of Contents

- [Features](#features)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the App](#running-the-app)
- [Deployment](#deployment)
- [License](#license)

---

## Features

### 🚀 FastAPI Backend
- **Asynchronous endpoints**: Built with FastAPI for high-performance and non-blocking I/O.
- **FastAPI-Users Integration**: Secure user registration, JWT authentication, password reset, and user verification.
- **SQLite Database**: Lightweight SQLite storage with async database sessions via SQLAlchemy (`aiosqlite`).
- **Media Upload Handler**: Robust validation and upload endpoint routing files directly to ImageKit.io.

### 📸 Streamlit Frontend
- **Clean Interactive UI**: Clean feed display, user dashboard, and intuitive upload panel.
- **Dynamic Media Transformation**: Direct integration with ImageKit text overlay/filters. Renders captions dynamically on images/videos using base64 URL-safe parameters.
- **Post Ownership & Safety**: Restricts deleting posts to the users who originally created them.

---

## How It Works

```
        User Browser (Streamlit App)
                     │
            (HTTP Requests)
                     ▼
          FastAPI Backend (main.py)
            ├── /auth/jwt/login  → JWT token generation
            ├── /auth/register   → Account creation
            ├── /feed            → SQLite Post retrieval
            ├── /posts/{id}      → Delete validation & cleanup
            └── /upload          → Temporarily caches, uploads to ImageKit
                     │
         ┌───────────┴───────────┐
         ▼                       ▼
   SQLite (test.db)      ImageKit.io (Media CDN)
(Stores URLs & Metas)    (Stores & transforms files)
```

---

## Project Structure

```
hackathon2_quick-pic/
├── main.py                # FastAPI entry point
├── frontend.py            # Streamlit frontend app
├── pyproject.toml         # Python project metadata & uv dependency configurations
├── requirements.txt       # Frozen dependencies (compiled from pyproject.toml)
├── uv.lock                # Lockfile for reproducible builds
├── .env                   # Environment variables (private keys, secrets)
├── test.db                # SQLite database file (local only)
└── app/
    ├── __init__.py
    ├── app.py             # FastAPI routes (feed, upload, delete, CORS configuration)
    ├── db.py              # SQLite configuration, database engines, and model declarations (User, Post)
    ├── images.py          # ImageKit SDK client configuration
    ├── schemas.py         # Pydantic schemas for request/response serialization
    └── users.py           # FastAPI-Users backend, user manager, and authentication pipeline
```

---

## Requirements

- Python **3.9+**
- [uv](https://docs.astral.sh/uv/) (highly recommended for dependency resolution) or `pip`
- ImageKit.io Free Account (for image hosting and overlays)

---

## Installation

### Using uv (recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/AayDexterous/2ndSwechaHackathon.git
   cd 2ndSwechaHackathon
   ```
2. Sync the project environment:
   ```bash
   uv sync
   ```

### Using pip

1. Clone the repository:
   ```bash
   git clone https://github.com/AayDexterous/2ndSwechaHackathon.git
   cd 2ndSwechaHackathon
   ```
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

Create a `.env` file in your project root to store secrets and keys:

```env
# ImageKit Credentials
IMAGEKIT_PRIVATE_KEY="your-private-key"
IMAGEKIT_PUBLIC_KEY="your-public-key"
IMAGEKIT_URL="https://ik.imagekit.io/your-endpoint"

# FastAPI JWT Secret Key
SECRET_KEY="your-jwt-signing-secret"

# Backend Endpoint (used by Streamlit)
BACKEND_URL="http://localhost:8000"
```

---

## Running the App

For local testing, run the backend and the frontend simultaneously in separate terminals:

### 1. Start the FastAPI Backend
```bash
python main.py
```
This launches the server at `http://localhost:8000`. You can visit `http://localhost:8000/docs` to view the interactive Swagger documentation.

### 2. Start the Streamlit Frontend
```bash
streamlit run frontend.py
```
This opens the frontend dashboard in your browser (typically at `http://localhost:8501`).

---

## Deployment

### Backend (Render)
1. Set up a new **Web Service** pointing to your GitHub repository.
2. Choose branch: `deploy`.
3. Configure the following parameters:
   - **Language**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.app:app --host 0.0.0.0 --port $PORT`
4. In **Environment Variables**, configure `IMAGEKIT_PRIVATE_KEY`, `IMAGEKIT_PUBLIC_KEY`, `IMAGEKIT_URL`, and `SECRET_KEY`.

### Frontend (Streamlit Community Cloud)
1. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/).
2. Select your repository and the `deploy` branch.
3. Set **Main file path** to `frontend.py`.
4. In **Advanced Settings -> Secrets**, configure the backend URL to point to your live Render endpoint:
   ```toml
   BACKEND_URL = "https://your-backend-app.onrender.com"
   ```

---

## License

This project is licensed under the MIT License.

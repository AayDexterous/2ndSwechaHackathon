# AGENTS.md — QuickPic (Simple Social)

This file describes the AI agent context for this repository: its purpose, architecture, conventions, and how an AI agent should navigate and modify it.

## Project Purpose

QuickPic is a simple social network application built for hackathons that allows users to register, log in, post images or videos with captions, view a feed of all posts, and delete their own posts. 

It is designed to run with a **FastAPI backend** (using SQLite database and ImageKit.io for media transformations) and a **Streamlit frontend** that communicates with the backend via HTTP REST requests.

---

## Architecture

```
main.py                              → FastAPI entrypoint (launches app.app:app)
frontend.py                          → Streamlit application (UI frontend)

app/
  app.py                             → Main FastAPI configuration & endpoints
                                       Endpoints: /upload, /feed, /posts/{post_id}, /
                                       Configures: CORSMiddleware, lifespan (DB tables init)
  db.py                              → Database setup (SQLAlchemy with aiosqlite)
                                       Models: User (FastAPI-Users model), Post
                                       Helper: create_db_and_tables(), get_async_session()
  images.py                          → ImageKit.io SDK initialization using env variables
  schemas.py                         → Pydantic models for request validation and serialization
                                       Models: PostCreate, PostResponse, UserRead, UserCreate, UserUpdate
  users.py                           → FastAPI-Users initialization
                                       Configures: UserManager, JWTStrategy, BearerTransport, auth_backend
```

---

## Data Flow

### 1. Authentication Flow (Register & Login)
```
User clicks Login/Register in Streamlit
  ➜ requests.post(f"{BACKEND_URL}/auth/register")
  ➜ requests.post(f"{BACKEND_URL}/auth/jwt/login") (returns JWT access_token)
  ➜ Streamlit saves access_token in st.session_state.token
  ➜ Streamlit requests f"{BACKEND_URL}/users/me" to retrieve User Info
```

### 2. Feed & Media Flow (Feed & Upload)
```
User uploads Image/Video with Caption in Streamlit
  ➜ requests.post(f"{BACKEND_URL}/upload") (includes JWT token header + files)
  ➜ FastAPI caches file temporarily in OS temp folder
  ➜ FastAPI uploads file to ImageKit.io via ImageKit SDK
  ➜ ImageKit returns URL (e.g. https://ik.imagekit.io/...)
  ➜ FastAPI saves Post metadata (URL, User ID, caption) to SQLite database
  ➜ User views feed ➜ requests.get(f"{BACKEND_URL}/feed")
  ➜ Streamlit requests transformed URL from ImageKit to display overlay text (caption)
```

---

## Key Conventions

### 1. Environment Variables
Always load variables from the environment with appropriate fallbacks for local development:
- `DATABASE_URL` (defaults to local SQLite `sqlite+aiosqlite:///./test.db`)
- `SECRET_KEY` (defaults to `aP9kL2fX8qZr` for JWT signing)
- `BACKEND_URL` (in frontend, defaults to `http://localhost:8000`)
- `IMAGEKIT_PRIVATE_KEY`, `IMAGEKIT_PUBLIC_KEY`, `IMAGEKIT_URL` (loaded directly in `app/images.py`)

### 2. Database Session Injection
Always use FastAPI dependency injection `Depends(get_async_session)` to get an async SQLAlchemy session. Do not construct session engines or sessionmakers inside route handlers directly.

### 3. Media Storage
Do not store uploaded media files locally in the project directory. All media files must be uploaded to ImageKit.io via `app/images.py`. Keep local filesystems clean by deleting any temporary buffers generated during transit (e.g., using python's `tempfile` and `os.unlink()`).

### 4. Cross-Origin Requests (CORS)
When adding new endpoints or altering response headers, keep the `CORSMiddleware` config intact in `app/app.py` so that external frontends can interact with the API.

---

## What NOT to Add

- **Direct Database Access from Streamlit**: Streamlit should never query the database directly. All database reading/writing must occur on the FastAPI backend through HTTP endpoints.
- **Persistent Local File Storage**: Do not build directories for storing uploads locally since Render instances have ephemeral filesystems and will lose these files on restart.
- **Plain Text Password Handling**: Always leverage the `fastapi-users` authentication backend (`users.py`) for managing, hashing, and verifying passwords.

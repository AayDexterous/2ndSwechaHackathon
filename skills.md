# Technical Skills Guide — QuickPic

This document outlines the core technical skills, libraries, and architectural concepts required to successfully develop, extend, and debug the QuickPic application.

---

## 1. Backend Development (FastAPI)

To maintain and extend the QuickPic API, developers should be proficient in:

- **Asynchronous Python (`async`/`await`)**: FastAPI is built for async execution. Database transactions and network calls must be non-blocking.
- **Route Handling & Dependency Injection**: FastAPI's `Depends` system is heavily used for database session lifecycle management and injecting the authenticated user object:
  ```python
  session: AsyncSession = Depends(get_async_session)
  user: User = Depends(current_active_user)
  ```
- **CORS Management**: Enabling CORS middleware to allow cross-origin communication between external frontends and the FastAPI server.

---

## 2. Database Management & ORM (SQLAlchemy & aiosqlite)

The database layers require skills in:

- **SQLAlchemy 2.0 (Async)**: Defining declarative async models using mappings, configuring relationships, and executing async queries:
  ```python
  # Async query execution
  result = await session.execute(select(Post).order_by(Post.created_at.desc()))
  posts = [row[0] for row in result.all()]
  ```
- **aiosqlite & SQLite**: Configuring async SQLite connections and running migration-free schema generation (`Base.metadata.create_all`) inside the FastAPI lifespan context.
- **UUID Handling**: Generating and working with database-backed UUIDs (instead of integer IDs) for security and uniqueness across entities.

---

## 3. User Authentication (FastAPI-Users)

Understanding security and user management:

- **FastAPI-Users Framework**: Setting up authentication adapters, DB adapters, and user schemas.
- **JWT Authentication**: Configuring `JWTStrategy` and `BearerTransport` to sign, verify, and validate access tokens.
- **Password Hashing**: Configuring automatic password hashing and verification using `argon2` or `bcrypt` via FastAPI-Users utilities.

---

## 4. Frontend & State Management (Streamlit)

For modifications to `frontend.py`:

- **Streamlit Session State**: Retaining tokens, user profiles, and login status across app reruns:
  ```python
  if 'token' not in st.session_state:
      st.session_state.token = None
  ```
- **Streamlit Components & Layouts**: Designing responsive UIs using `st.columns`, `st.sidebar`, and rendering lists of items dynamically using loops.
- **Inter-service API Calls**: Communicating with the backend using the python `requests` library and passing JWT tokens via Bearer headers.

---

## 5. Media Management & Transformations (ImageKit.io SDK)

QuickPic utilizes third-party image transformation hosting:

- **ImageKit SDK Integration**: Interfacing with the ImageKit Python SDK using credentials securely loaded from environment variables.
- **Dynamic Transforms**: Dynamically applying resizing parameters and generating base64/URL-safe watermarks and text overlays for captions directly within the image URL path:
  ```python
  # base64 overlay injection format
  text_overlay = f"l-text,ie-{encoded_caption},ly-N20,lx-20,fs-100,co-white,bg-000000A0,l-end"
  ```

---

## 6. Packaging & Environments (uv / pip)

- **uv Package Manager**: Building environments, resolving dependencies, and compiling locked package requirements (`uv pip compile`).
- **Environment Isolation**: Setting up and activating virtual environments (`.venv`).
- **Configuration Management**: Sourcing variables dynamically from `.env` files using `python-dotenv`.

# MultiModal RAG Research Assistant

An AI research workspace for uploading PDFs and images, asking grounded questions, searching indexed passages, summarizing papers, comparing documents, and generating study notes.

## Architecture

```text
Next.js + React + TypeScript frontend
              ↓ REST API
       Existing FastAPI backend
              ↓
 LangChain · LangGraph · Gemini · ChromaDB
              ↓
 PDF extraction · OCR · embeddings · retrieval
```

The frontend is a client for the existing FastAPI API. All document processing and AI/RAG work remains in the backend.

## Features

- PDF and image uploads with multi-file support
- Indexed document listing and deletion
- RAG chat with backend citations
- Semantic retrieval of source passages
- Document summarization and comparison
- Configurable study-note generation
- Light and dark themes, responsive navigation, and mobile layout

## Requirements

- Python 3.10+ and backend dependencies from `backend/requirements.txt`
- Node.js 20+
- A Gemini API key configured only in the backend

## Run locally

Use two terminals from the repository root. The FastAPI backend and the Next.js frontend run as separate processes.

### 1. Configure and run the backend

Create the environment file, then add your Gemini API key. Keep this file private; it is ignored by Git.

```bash
cd backend
# Windows PowerShell:
Copy-Item .env.example .env
# macOS/Linux instead:
# cp .env.example .env
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# macOS/Linux instead:
# source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

FastAPI runs at [http://127.0.0.1:8000](http://127.0.0.1:8000), with API documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

### 2. Configure and run the frontend

In a second terminal, from the repository root:

```bash
cd frontend
copy .env.example .env.local
npm ci
npm run dev
```

If you use macOS/Linux, use `cp .env.example .env.local` instead of `copy`. Confirm `frontend/.env.local` contains `NEXT_PUBLIC_API_URL=http://127.0.0.1:8000`. Next.js runs at [http://localhost:3000](http://localhost:3000). Restart the frontend after changing this variable.

### 3. Use Docker instead

After Docker Desktop is running and `backend/.env` is configured:

```bash
docker compose up --build
```

Open the same frontend and backend URLs above. To point the browser at a different backend origin, set `NEXT_PUBLIC_API_URL` before building the frontend image.

## API integration

The centralized client in `frontend/lib/api.ts` uses these existing endpoints:

| Feature | Endpoint |
| --- | --- |
| Health status | `GET /health` |
| Upload PDFs / images | `POST /upload/pdf`, `POST /upload/image` (`files` multipart field) |
| List documents | `GET /upload/pdfs`, `/upload/images`, `/upload/documents` |
| Delete indexed document | `DELETE /upload/document/{filename}` |
| RAG chat | `POST /query` (`question`, `top_k`) |
| Semantic retrieval | `POST /query/retrieve` (`question`, `top_k`) |
| Summarization | `POST /summarize` (`filename`) |
| Comparison | `POST /compare` (`document_1`, `document_2`) |
| Study notes | `POST /notes` (`filename`, `note_type`) |

The backend enables CORS for all origins already, so no backend CORS change was needed. Keep all model keys and backend secrets in `backend/.env`; do not use `NEXT_PUBLIC_` for secrets.

Removing a document from the Documents page removes its indexed chunks from ChromaDB. The original uploaded file remains in the backend upload folder because the existing API only deletes the index entry.

### Troubleshooting

- If the frontend reports that the research service is unavailable, start FastAPI and confirm `NEXT_PUBLIC_API_URL` points to its reachable address.
- If you edit `frontend/.env.local`, restart Next.js so it reads the updated setting.
- If Docker cannot connect to its engine, start Docker Desktop before running Compose.

## Docker

The Compose stack exposes FastAPI on port 8000 and Next.js on port 3000:

```bash
docker compose build
docker compose up -d
docker compose logs -f
docker compose down
```

The browser frontend uses `http://localhost:8000` as its API URL. The backend container and its data, vector database, and logs remain as configured in `docker-compose.yml`.

## Backend configuration

Create `backend/.env` from `backend/.env.example`. Configure the backend values there, including:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
GEMINI_MODEL=gemini-2.5-flash
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
CHROMA_DB_PATH=vectordb
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K=5
```

The frontend requires only the public API origin; it does not handle backend credentials. For Docker, set the public frontend API origin at build time with `NEXT_PUBLIC_API_URL` if the browser should reach FastAPI at an address other than `http://localhost:8000`.

## Project structure

```text
backend/       FastAPI routes and existing RAG/document services
frontend/app/  Next.js App Router UI and design system
frontend/lib/  Typed centralized REST API client
docker-compose.yml
```

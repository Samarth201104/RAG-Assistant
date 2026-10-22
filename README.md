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

### Backend

Create `backend/.env` with the settings described in `backend/.env.example`, including `GEMINI_API_KEY`, then:

```bash
cd backend
pip install -r requirements.txt
python main.py
```

FastAPI runs at [http://127.0.0.1:8000](http://127.0.0.1:8000), with API documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Next.js runs at [http://localhost:3000](http://localhost:3000). Set `NEXT_PUBLIC_API_URL` in `frontend/.env.local` to the FastAPI origin. The default is `http://127.0.0.1:8000`.

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

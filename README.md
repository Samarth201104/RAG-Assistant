# 🤖 MultiModal RAG Research Assistant

An enterprise-grade **MultiModal Retrieval-Augmented Generation (RAG)** application that enables users to upload PDFs and images, perform semantic search, ask context-aware questions, generate summaries, compare documents, and create study notes using **FastAPI**, **LangChain**, **Gemini**, **ChromaDB**, and **Sentence Transformers**.

---

# 🚀 Features

- 📄 Upload PDF documents
- 🖼️ Upload images with OCR support
- 💬 Context-aware AI Chat
- 📚 Semantic Search using Vector Embeddings
- 📝 AI-powered Document Summarization
- ⚖️ Multi-document Comparison
- 📖 Automatic Study Notes Generation
- 🔍 Citation-aware Responses
- 🧠 ChromaDB Vector Database
- ⚡ FastAPI Backend
- 🎨 Streamlit Frontend
- 🐳 Docker & Docker Compose Support

---

# 🏗️ System Architecture

```
                        User
                          │
                          ▼
                Streamlit Frontend
                          │
                    REST API Calls
                          │
                          ▼
                  FastAPI Backend
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
   PDF Processing     Image OCR         Gemini 2.5 Flash
      (PyMuPDF)      (EasyOCR)              LLM
        │                 │
        └────────────┬────┘
                     ▼
             Text Chunking
                     ▼
      Sentence Transformer Embeddings
                     ▼
              Chroma Vector Database
                     ▼
            Semantic Retrieval (RAG)
                     ▼
              AI Generated Response
```

---

# 🛠 Tech Stack

## Backend

- FastAPI
- LangChain
- LangGraph
- Gemini 2.5 Flash
- ChromaDB
- Sentence Transformers
- EasyOCR
- PyMuPDF
- OpenCV
- Pillow

## Frontend

- Streamlit

## AI / ML

- Retrieval-Augmented Generation (RAG)
- Semantic Search
- Vector Embeddings
- OCR
- Prompt Engineering

## Deployment

- Docker
- Docker Compose

---

# 📂 Project Structure

```
RAG-System/
│
├── backend/
│   ├── api/
│   ├── core/
│   ├── data/
│   ├── logs/
│   ├── models/
│   ├── prompts/
│   ├── services/
│   ├── utils/
│   ├── vectordb/
│   ├── vectorstore/
│   ├── Dockerfile
│   ├── main.py
│   ├── requirements.txt
│   └── requirements-docker.txt
│
├── frontend/
│   ├── assets/
│   ├── components/
│   ├── services/
│   ├── utils/
│   ├── views/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

# ⚙️ Local Installation

## 1. Clone Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd RAG-System
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

---

## 4. Install Frontend Dependencies

```bash
cd ../frontend
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

## Backend

Create

```
backend/.env
```

Example

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY

GEMINI_MODEL=gemini-2.5-flash

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

CHROMA_DB_DIRECTORY=vectordb

CHUNK_SIZE=1000

CHUNK_OVERLAP=200

TOP_K=5
```

---

## Frontend

Create

```
frontend/.env
```

Example

```env
BACKEND_URL=http://127.0.0.1:8000
```

---

# 🔐 Get Gemini API Key

1. Visit **Google AI Studio**
2. Sign in with your Google account.
3. Generate an API key.
4. Copy the key.
5. Paste it into

```
backend/.env
```

---

# ▶️ Running the Application

## Start Backend

```bash
cd backend

python main.py
```

Backend

```
http://127.0.0.1:8000
```

Swagger

```
http://127.0.0.1:8000/docs
```

---

## Start Frontend

```bash
cd frontend

streamlit run app.py
```

Frontend

```
http://localhost:8501
```

---

# 🐳 Docker Deployment

## Build Containers

```bash
docker compose build
```

---

## Start Containers

```bash
docker compose up -d
```

---

## Stop Containers

```bash
docker compose down
```

---

## View Logs

```bash
docker compose logs -f
```

---

## Restart Containers

```bash
docker compose restart
```

---

# 📌 Docker Architecture

The project uses **two Docker containers**.

| Container | Purpose |
|------------|----------|
| Backend | FastAPI + LangChain + Gemini + ChromaDB |
| Frontend | Streamlit UI |

Communication occurs over the internal Docker network.

```
Frontend
http://backend:8000
        │
        ▼
Backend
```

---

# 📖 API Documentation

Swagger UI

```
http://localhost:8000/docs
```

Includes APIs for

- Health
- Upload PDF
- Upload Image
- Chat
- Summarize
- Compare
- Notes

---

# ✨ Application Workflow

1. Upload PDFs or Images.
2. Extract text.
3. Perform OCR (for images).
4. Split into semantic chunks.
5. Generate vector embeddings.
6. Store embeddings in ChromaDB.
7. Retrieve relevant chunks.
8. Send retrieved context to Gemini.
9. Generate context-aware responses with citations.

---

# 👨‍💻 Author

**Samarth More**

Artificial Intelligence & Machine Learning Engineer

GitHub:
> Add your GitHub profile

LinkedIn:
> Add your LinkedIn profile

---

# 📄 License

This project is intended for educational, research, and portfolio purposes.
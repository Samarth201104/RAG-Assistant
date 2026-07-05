# RAG System

A Retrieval-Augmented Generation (RAG) system for document processing, embedding, and intelligent querying.

## Project Structure

```
RAG-System/
├── backend/                    # FastAPI backend
│   ├── api/                    # API endpoints
│   ├── core/                   # Core configuration and utilities
│   ├── services/               # Business logic services
│   ├── vectorstore/            # Vector database management
│   ├── models/                 # Request/response models
│   ├── utils/                  # Utility functions
│   └── main.py                 # Application entry point
├── frontend/                   # Streamlit UI
│   ├── streamlit_app.py        # Main app
│   └── pages/                  # App pages
├── data/                       # Data storage
│   ├── pdfs/                   # PDF files
│   └── images/                 # Image files
├── vectordb/                   # Vector database
├── logs/                       # Application logs
└── requirements.txt            # Python dependencies
```

## Features

- **Document Upload**: Upload PDF and image files
- **RAG Querying**: Query documents using retrieval-augmented generation
- **Summarization**: Generate summaries from documents
- **Document Comparison**: Compare multiple documents
- **Notes Management**: Create and manage notes
- **Citation Tracking**: Track and manage citations

## Getting Started

### Installation

```bash
pip install -r requirements.txt
```

### Configuration

Create a `.env` file with your configuration:

```env
API_HOST=0.0.0.0
API_PORT=8000
CHROMA_PERSIST_DIRECTORY=./vectordb
LLM_MODEL=gpt-3.5-turbo
EMBEDDING_MODEL=text-embedding-3-small
```

### Running the Application

**Backend (FastAPI):**
```bash
python backend/main.py
```

**Frontend (Streamlit):**
```bash
streamlit run frontend/streamlit_app.py
```

## API Endpoints

- `POST /api/upload/pdf` - Upload PDF
- `POST /api/upload/image` - Upload image
- `POST /api/query/search` - Search query
- `POST /api/summarize/document` - Summarize document
- `POST /api/compare/documents` - Compare documents
- `POST /api/notes/create` - Create note

## Technology Stack

- **Backend**: FastAPI, Pydantic
- **Frontend**: Streamlit
- **Vector Store**: Chroma
- **Embeddings**: OpenAI API
- **LLM**: OpenAI GPT-3.5-turbo
- **PDF Processing**: pdf2image, pytesseract
- **OCR**: Tesseract

## Development

For development, install additional dependencies:

```bash
pip install pytest pytest-asyncio black flake8
```

## License

This project is licensed under the MIT License.

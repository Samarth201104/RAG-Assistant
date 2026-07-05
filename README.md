# RAG System

This project is a Retrieval-Augmented Generation (RAG) application that helps users upload documents, retrieve relevant information, and ask questions using AI. It combines a FastAPI backend with a Streamlit frontend for a simple document-based assistant experience.

## Features

- Upload PDF and image documents
- Ask questions about uploaded content
- Generate document summaries
- Compare multiple documents
- Create and manage notes
- View citations for generated answers

## Installation

1. Clone the repository.
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the project root by copying the example file:
   ```bash
   copy .env.example .env
   ```
   Then open the `.env` file and replace the placeholder value for `GEMINI_API_KEY` with your real key.
5. Generate a Gemini API key:
   - Go to the Google AI Studio website.
   - Sign in with your Google account.
   - Create a new API key from the "Get API Key" section.
   - Copy the generated key and paste it into the `.env` file.
6. Run the backend:
   ```bash
   python backend/main.py
   ```
7. Run the frontend:
   ```bash
   streamlit run frontend/app.py
   ```


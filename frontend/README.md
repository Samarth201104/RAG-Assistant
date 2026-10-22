# Atlas Research frontend

Next.js App Router client for the existing FastAPI REST API. Configure `NEXT_PUBLIC_API_URL` before starting. The default is `http://127.0.0.1:8000`.

```bash
npm install
npm run dev
```

The browser calls FastAPI directly. Backend credentials belong only in `backend/.env` and must never be exposed through frontend environment variables.

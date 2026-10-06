# Marginalia — study workspace (CBSE / ICSE)
Next.js + TS + Tailwind · FastAPI · PostgreSQL. All curriculum and questions are **generated sample content**, not official CBSE/ICSE material.

## Run
1. `cp .env.example .env` ; `docker compose up -d db`
2. Backend: `cd backend && python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt && uvicorn app.main:app --reload` (seeds curriculum on first start)
3. Frontend: `cd frontend && npm i && NEXT_PUBLIC_API_URL=http://localhost:8000 npm run dev` → http://localhost:3000

## Notes
- Solve: typed text, image (needs `tesseract` installed for OCR), PDF (pypdf). Equations/arithmetic are solved with SymPy and **verified by substitution** before display; unsupported questions are reported as such, never faked.
- Password reset: token is logged to the backend console (no email provider configured).
- Not yet built: full curriculum depth (seed is a small generated outline per board/class), non-math question content (placeholder concept checks), email delivery, automated tests.

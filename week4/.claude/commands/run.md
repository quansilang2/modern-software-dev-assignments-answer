# Run the Development Server

Start the FastAPI development server with auto-reload enabled.

## Command

```bash
cd week4 && python -m uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

## Notes

- Server runs on http://127.0.0.1:8000
- API docs available at http://127.0.0.1:8000/docs
- Frontend available at http://127.0.0.1:8000/
- Auto-reload enabled for development
- Press CTRL+C to stop the server

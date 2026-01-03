# Week 4: Developer's Command Center

This is a FastAPI + SQLite starter application for practicing Claude Code automations.

## Project Structure

```
week4/
├── backend/                    # FastAPI application
│   └── app/
│       ├── main.py            # Application entry point, FastAPI app setup
│       ├── db.py              # Database configuration (SQLite + SQLAlchemy)
│       ├── models.py          # ORM models (Note, ActionItem)
│       ├── schemas.py         # Pydantic schemas for request/response validation
│       ├── routers/           # API route handlers
│       │   ├── notes.py       # Notes CRUD endpoints
│       │   └── action_items.py # Action items endpoints
│       └── services/          # Business logic
│           └── extract.py     # Extract action items from text
├── frontend/                   # Static HTML/JS/CSS (no Node.js needed)
│   ├── index.html            # Main UI
│   ├── app.js                # Frontend logic
│   └── styles.css            # Styling
├── data/                      # SQLite database and seed files
│   └── seed.sql              # Initial database seed data
├── docs/                      # Documentation
│   └── TASKS.md              # Practice tasks for the application
└── tests/                     # pytest test files
    └── backend/
        └── tests/
            ├── conftest.py   # Test fixtures
            ├── test_notes.py
            └── test_action_items.py
```

## Quick Start

### Running the Application
```bash
# From week4/ directory
python -m uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

Then visit:
- Frontend: http://127.0.0.1:8000/
- API Docs: http://127.0.0.1:8000/docs

### Running Tests
```bash
# Run all tests
python -m pytest backend/tests -v

# Run with coverage
python -m pytest backend/tests --cov=backend/app --cov-report=term-missing

# Run specific test file
python -m pytest backend/tests/test_notes.py -v
```

### Code Quality
```bash
# Format code
python -m black .

# Check linting
python -m ruff check .

# Auto-fix linting issues
python -m ruff check . --fix
```

## Code Style Guidelines

### Python Style
- Use **black** for formatting (automatically applied via pre-commit)
- Use **ruff** for linting (faster replacement for flake8, pylint, etc.)
- Follow PEP 8 conventions
- Use type hints where appropriate
- Maximum line length: 88 characters (black default)

### FastAPI Patterns
- All routes use Pydantic schemas for request/response validation
- Database operations use SQLAlchemy ORM with `get_db()` dependency
- Routes are organized in `backend/app/routers/` by feature
- Use `HTTPException` for error responses with appropriate status codes

### Testing Patterns
- Use `TestClient` from `fastapi.testclient` for endpoint testing
- Test fixtures are in `backend/tests/conftest.py`
- Test files follow the pattern `test_*.py`
- Each endpoint should have tests for:
  - Success cases
  - Validation errors (400)
  - Not found cases (404)

## Common Workflows

### Adding a New API Endpoint

When asked to add a new API endpoint:

1. **Write the test first** in `backend/tests/test_*.py`:
   ```python
   def test_new_endpoint(client):
       response = client.get("/new-endpoint")
       assert response.status_code == 200
   ```

2. **Implement the route** in `backend/app/routers/*.py`:
   - Create Pydantic schemas in `schemas.py` if needed
   - Add the route function with proper type hints
   - Use `get_db()` dependency for database access

3. **Run tests** to verify:
   ```bash
   python -m pytest backend/tests -v
   ```

4. **Run pre-commit hooks**:
   ```bash
   python -m black .
   python -m ruff check . --fix
   ```

### Adding a New Database Model

1. **Define the model** in `backend/app/models.py`:
   ```python
   class NewModel(Base):
       __tablename__ = "new_table"
       id = Column(Integer, primary_key=True)
       # ... other columns
   ```

2. **Create Pydantic schemas** in `backend/app/schemas.py`:
   - `NewModelCreate` for input validation
   - `NewModelRead` for response serialization

3. **Create router** in `backend/app/routers/new_model.py`

4. **Register router** in `backend/app/main.py`:
   ```python
   from .routers import new_model as new_model_router
   app.include_router(new_model_router.router)
   ```

### Database Seeding

The database is automatically seeded on startup if it doesn't exist. To re-seed:
```bash
# Delete the database file
rm data/app.db

# Restart the application
python -m uvicorn backend.app.main:app --reload
```

## Safety Guidelines

### Safe Commands
- `python -m pytest backend/tests` - Run tests
- `python -m black .` - Format code
- `python -m ruff check .` - Check linting
- `python -m ruff check . --fix` - Auto-fix linting
- `python -m uvicorn backend.app.main:app --reload` - Run dev server

### Commands to Avoid
- DO NOT use `pytest` without `python -m` (may use wrong environment)
- DO NOT use `black` without `python -m` (may use wrong environment)
- DO NOT use `ruff` without `python -m` (may use wrong environment)
- DO NOT manually modify `data/app.db` (use ORM or seed.sql)
- DO NOT commit unformatted code (run pre-commit first)

### Pre-commit Hooks
Pre-commit hooks are configured in `.pre-commit-config.yaml`:
- black: Code formatting
- ruff: Linting with auto-fix
- end-of-file-fixer: Ensures files end with newline
- trailing-whitespace: Removes trailing whitespace

Install pre-commit hooks:
```bash
pre-commit install
```

Run pre-commit on all files:
```bash
pre-commit run --all-files
```

## Current API Endpoints

### Notes
- `GET /notes/` - List all notes
- `POST /notes/` - Create a new note
- `GET /notes/search/` - Search notes (query param: `q`)
- `GET /notes/{id}` - Get a specific note

### Action Items
- `GET /action-items/` - List all action items
- `POST /action-items/` - Create a new action item
- `PUT /action-items/{id}/complete` - Mark an action item as complete

## Extension Tasks

See `docs/TASKS.md` for practice tasks including:
- Pre-commit setup and repo fixes
- Search endpoint enhancements
- Action item completion flow
- Extraction logic improvements
- CRUD enhancements
- Request validation and error handling
- Documentation maintenance

## Available Slash Commands

From the repository root, you can use:
- `/test-format` - Run tests, format code, check lint, generate coverage
- `/run` - Start the development server
- `/test` - Run tests with optional parameters
- `/format` - Format code with black and ruff
- `/lint` - Check for linting issues

## Notes

- This project uses **Python 3.12+**
- Database is **SQLite** (file-based, no server needed)
- Frontend is **vanilla JavaScript** (no build step required)
- All dependencies are listed via `pip install` commands
- The application automatically creates the database on first run

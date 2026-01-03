# Assignments for CS146S: The Modern Software Developer

This is the home of the assignments for [CS146S: The Modern Software Developer](https://themodernsoftware.dev), taught at Stanford University fall 2025.

## Repo Setup
These steps work with Python 3.12.

1. Install Anaconda
   - Download and install: [Anaconda Individual Edition](https://www.anaconda.com/download)
   - Open a new terminal so `conda` is on your `PATH`.

2. Create and activate a Conda environment (Python 3.12)
   ```bash
   conda create -n cs146s python=3.12 -y
   conda activate cs146s
   ```

3. Install Poetry
   ```bash
   curl -sSL https://install.python-poetry.org | python -
   ```

4. Install project dependencies with Poetry (inside the activated Conda env)
   From the repository root:
   ```bash
   poetry install --no-interaction
   ```

---

## Week 4: Autonomous Coding Agent with Claude Code

This folder demonstrates the use of **Claude Code automations** to streamline development workflows.

### Quick Start (Week 4)

```bash
# Navigate to week4 directory
cd week4

# Install dependencies
pip install fastapi sqlalchemy pytest pydantic python-dotenv httpx
pip install pytest-cov black ruff uvicorn

# Run the application
python -m uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

Visit:
- **Frontend**: http://127.0.0.1:8000/
- **API Docs**: http://127.0.0.1:8000/docs

### Automations Overview

Week 4 includes **3 Claude Code automations**:

#### Automation #1: Custom Slash Commands

Reusable workflows invoked with `/` in Claude Code.

| Command | Description |
|---------|-------------|
| `/test-format` | Run tests → format → lint → coverage |
| `/run` | Start development server |
| `/test` | Run tests |
| `/format` | Format code |
| `/lint` | Check linting |

**Usage**: In Claude Code, simply type `/test-format`

#### Automation #2: CLAUDE.md Repository Guidance

`week4/CLAUDE.md` provides project-specific context that Claude Code automatically reads.

**Benefits**:
- Claude knows the project structure
- Follows established patterns automatically
- Uses safe commands
- Writes tests first (TDD)

#### Automation #3: SubAgents

Specialized AI assistants that collaborate on development tasks.

**Architecture**:
```
TestAgent (QA) → CodeAgent (Dev) → TestAgent (Verify)
```

**Usage**:
```bash
/feature-dev Add PUT /notes/{id} endpoint
```

### Project Structure (Week 4)

```
week4/
├── CLAUDE.md                     # Repository guidance
├── writeup.md                    # Assignment documentation
├── backend/                      # FastAPI application
│   └── app/
│       ├── main.py              # App setup
│       ├── models.py            # Database models
│       ├── schemas.py           # Pydantic schemas
│       └── routers/             # API endpoints
├── backend/tests/                # Test files
├── frontend/                     # Static UI
└── docs/                         # Documentation
```

### Running Tests

```bash
cd week4

# Run all tests
python -m pytest backend/tests -v

# Run with coverage
python -m pytest backend/tests --cov=backend/app --cov-report=term-missing
```

### Documentation

For complete Week 4 documentation, see:
- `week4/assignment.md` - Assignment instructions
- `week4/writeup.md` - Automation details
- `week4/CLAUDE.md` - Project context
- `.claude/agents/technical-explanation.md` - SubAgent technical details
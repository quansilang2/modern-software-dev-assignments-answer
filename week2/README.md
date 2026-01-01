# Action Item Extractor

A FastAPI-based application that extracts actionable items (todos) from free-form meeting notes. It supports both rule-based heuristic extraction and LLM-powered extraction (using Ollama).

## Features

-   **Action Item Extraction**: automatically identifies tasks from bullet points, checkboxes, and imperative sentences.
-   **LLM Integration**: Optional "Agentic Mode" uses a local Large Language Model (e.g., Llama 3) for more intelligent extraction.
-   **Note Management**: Save raw notes and track the completion status of extracted items.
-   **Web Interface**: Simple HTML/JS frontend for interacting with the API.

## Project Structure

```
week2/
├── app/
│   ├── routers/        # API route definitions
│   │   ├── action_items.py
│   │   └── notes.py
│   ├── services/       # Core business logic
│   │   └── extract.py  # Extraction algorithms (Rule-based & LLM)
│   ├── db.py           # Database connection and CRUD operations
│   └── main.py         # App entry point
├── frontend/           # Static HTML frontend
├── tests/              # Unit tests
└── data/               # SQLite database storage (generated)
```

## Setup and Installation

1.  **Prerequisites**:
    *   Python 3.8+
    *   [Poetry](https://python-poetry.org/) (recommended) or Conda
    *   [Ollama](https://ollama.com/) (for LLM features)

2.  **Environment Setup**:
    ```bash
    # Activate your environment (e.g., conda)
    conda activate cs146s
    
    # Install dependencies
    poetry install
    ```

3.  **Ollama Setup** (Optional for LLM features):
    *   Install Ollama from [ollama.com](https://ollama.com).
    *   Pull the default model (e.g., llama3.1):
        ```bash
        ollama run llama3.1
        ```

## Running the Application

1.  Start the FastAPI server:
    ```bash
    poetry run uvicorn week2.app.main:app --reload
    ```
    The server will start at `http://127.0.0.1:8000`.

2.  Open your browser and navigate to `http://127.0.0.1:8000` to use the web interface.

## API Endpoints

### Action Items
-   `POST /action-items/extract`: Extract action items using rule-based heuristics.
-   `POST /action-items/extract-llm`: Extract action items using a local LLM.
-   `POST /action-items/{id}/done`: Mark an action item as completed.

### Notes
-   `GET /notes`: List all saved notes.
-   `GET /notes/{id}`: Get a specific note by ID.
-   `POST /notes`: Create a new note manually (mostly used internally by extract endpoints).

## Running Tests

Run the test suite using `pytest`:

```bash
poetry run pytest
```

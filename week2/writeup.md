# Week 2 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: James Bond \
SUNet ID: jbond \
Citations: AI Assistant (for code generation and refactoring support), FastAPI docs, Ollama docs.

This assignment took me about 1 hour to do. 


## YOUR RESPONSES
For each exercise, please include what prompts you used to generate the answer, in addition to the location of the generated response. Make sure to clearly add comments in your code documenting which parts are generated.

### Exercise 1: Scaffold a New Feature
Prompt: 
```
Extract all action items (todo items, tasks) from the following note text.
Only extract clear, actionable items. Ignore completed items and general descriptions.

Note text:
{text}

Return the result as a JSON array of strings. Format: ["item1", "item2", "item3"]
Return only the JSON array, no additional explanation.
``` 

Generated Code Snippets:
```
week2/app/services/extract.py: L92-242 (Implemented extract_action_items_llm function)
```

### Exercise 2: Add Unit Tests
Prompt: 
```
Write unit tests for `extract_action_items_llm()` covering multiple inputs (e.g., bullet lists, keyword-prefixed lines, empty input).
Ensure tests verifying that the function returns a list of strings and handles various input formats correctly.
``` 

Generated Code Snippets:
```
week2/tests/test_extract.py: L22-72 (Added tests for LLM extraction)
```

### Exercise 3: Refactor Existing Code for Clarity
Prompt: 
```
Refactor the backend code to improve modularity and clarity. 
Separating the database logic into a dedicated module (`db.py`) and organize API routes into a `routers` package (`routers/notes.py`, `routers/action_items.py`). 
Ensure consistent error handling and clear separation of concerns.
``` 

Generated/Modified Code Snippets:
```
week2/app/main.py: L1-30 (Simplified entry point, includes routers)
week2/app/db.py: L1-117 (Encapsulated database connection and CRUD operations)
week2/app/routers/notes.py: L1-35 (New router for notes endpoints)
week2/app/routers/action_items.py: L1-51 (New router for action items endpoints)
```


### Exercise 4: Use Agentic Mode to Automate a Small Task
Prompt: 
```
1. Integrate the LLM-powered extraction as a new endpoint. Update the frontend to include an "Extract LLM" button that, when clicked, triggers the extraction process via the new endpoint.
2. Expose one final endpoint to retrieve all notes. Update the frontend to include a "List Notes" button that, when clicked, fetches and displays them.
``` 

Generated Code Snippets:
```
week2/app/routers/action_items.py: L28-40 (Added /extract-llm endpoint)
week2/app/routers/notes.py: L13-24 (Added GET /notes endpoint)
week2/frontend/index.html: L26-27, L35-97 (Added buttons and JS handlers for LLM extraction and listing notes)
```


### Exercise 5: Generate a README from the Codebase
Prompt: 
```
Use Cursor to analyze the current codebase and generate a well-structured README.md file. The README should include, at a minimum:
- A brief overview of the project
- How to set up and run the project
- API endpoints and functionality
- Instructions for running the test suite
``` 

Generated Code Snippets:
```
week2/README.md: L1-67 (Generated entire README file)
```


## SUBMISSION INSTRUCTIONS
1. Hit a `Command (⌘) + F` (or `Ctrl + F`) to find any remaining `TODO`s in this file. If no results are found, congratulations – you've completed all required fields. 
2. Make sure you have all changes pushed to your remote repository for grading.
3. Submit via Gradescope. 
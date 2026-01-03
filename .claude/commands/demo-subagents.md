# Demo: SubAgent Collaboration

Demonstrate TestAgent and CodeAgent working together to add a simple feature.

## Feature to Implement

Add a **PUT /notes/{id}** endpoint to update existing notes.

---

## Phase 1: TestAgent (You are now TestAgent)

Read `.claude/agents/test-agent.md` for your instructions.

Your task:
1. Write tests for PUT /notes/{id} endpoint in `week4/backend/tests/test_notes.py`
2. Test scenarios:
   - Successful update (200)
   - Update non-existent note (404)
   - Update with invalid data (400)
3. Run tests to confirm they fail
4. Report: "Tests written. Ready for CodeAgent."

---

## Phase 2: CodeAgent (After TestAgent finishes)

Read `.claude/agents/code-agent.md` for your instructions.

Your task:
1. Read the failing tests from TestAgent
2. Implement PUT /notes/{id} endpoint in `week4/backend/app/routers/notes.py`
3. Add NoteUpdate schema to `week4/backend/app/schemas.py` if needed
4. Run tests to verify they pass
5. Run format and lint
6. Report: "Implementation complete. Tests passing."

---

## Phase 3: TestAgent Verification

Your task:
1. Run full test suite
2. Run coverage report
3. Verify coverage is adequate
4. Final report with results

---

## Expected Flow

```
User: /demo-subagents

[TestAgent]
→ Writes tests for PUT endpoint
→ Runs tests - they fail (red)
→ "Tests written for PUT /notes/{id}. 3 test cases added."

[CodeAgent]
→ Reads test requirements
→ Implements PUT endpoint
→ Adds NoteUpdate schema
→ Runs tests - they pass (green)
→ "PUT endpoint implemented. All tests passing."

[TestAgent]
→ Verifies coverage: 95%
→ "Feature complete. All tests passing. Coverage: 95%"
```

## Instructions

Use `/clear` between phase switches to reset context.
Read the appropriate agent config file at the start of each phase.

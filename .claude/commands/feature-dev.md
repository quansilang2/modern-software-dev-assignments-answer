# Feature Development with SubAgents

Implement a new feature using TestAgent and CodeAgent collaboration.

## Process

This command orchestrates a two-agent workflow:

1. **TestAgent** writes tests for the feature
2. **CodeAgent** implements the feature to make tests pass
3. **TestAgent** verifies tests pass and coverage is adequate

## Steps

### Phase 1: TestAgent

Act as **TestAgent** (see `.claude/agents/test-agent.md`):

1. Understand the feature request from $ARGUMENTS
2. Write comprehensive tests in `week4/backend/tests/test_*.py`
3. Include tests for:
   - Success cases (200, 201)
   - Validation errors (400)
   - Not found cases (404)
   - Edge cases
4. Run the tests to confirm they fail (red state)
5. Summarize what tests were written

### Phase 2: CodeAgent

Switch to **CodeAgent** role (see `.claude/agents/code-agent.md`):

1. Review the failing tests written by TestAgent
2. Implement the feature in `week4/backend/app/`:
   - Add schemas to `schemas.py` if needed
   - Add routes to appropriate router file
   - Follow existing patterns in the codebase
3. Run tests to verify they now pass
4. Run formatting: `cd week4 && python -m black .`
5. Run linting: `cd week4 && python -m ruff check . --fix`
6. Summarize what was implemented

### Phase 3: Verification

Return to **TestAgent** role:

1. Run full test suite: `cd week4 && python -m pytest backend/tests -v`
2. Run coverage report: `cd week4 && python -m pytest backend/tests --cov=backend/app --cov-report=term-missing`
3. Verify coverage is 80%+ for affected modules
4. Report final status

## Example Usage

```
/feature-dev Add DELETE endpoint for notes
```

```
/feature-dev Add PUT /notes/{id} to update notes
```

```
/feature-dev Add validation to ensure note title is not empty
```

## Coordination Notes

- Use `/clear` between agent role switches for fresh context
- Each agent should read their configuration file at the start
- Agents should communicate clearly at handoff points
- Final report should include:
  - What was tested
  - What was implemented
  - Test results (pass/fail)
  - Coverage percentage
  - Any remaining issues

## Files Referenced

- `.claude/agents/test-agent.md` - TestAgent instructions
- `.claude/agents/code-agent.md` - CodeAgent instructions
- `week4/CLAUDE.md` - Project context and guidelines

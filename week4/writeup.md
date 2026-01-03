# Week 4 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: **Your Name** \
SUNet ID: **your-sunet** \
Citations: [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices), [SubAgents Documentation](https://code.claude.com/docs/en/sub-agents)

This assignment took me about **4-6** hours to do. 


## YOUR RESPONSES
### Automation #1: Custom Slash Commands

**a. Design inspiration**

Inspired by the [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices) guide, which emphasizes creating slash commands for repeated workflows. The guide recommends: "Use custom slash commands to automate repetitive tasks" and "Turn repeated instructions into shortcuts."

**b. Design of each automation**

**Goal:** Streamline the development workflow by automating testing, formatting, linting, and coverage reporting into a single command.

**Commands Created:**
1. `/test-format` - Run tests, format code, check lint, and generate coverage report
2. `/run` - Start the development server
3. `/test` - Run tests with optional parameters
4. `/format` - Format code with black and ruff
5. `/lint` - Check for linting issues

**Inputs/Outputs:**
- **Input:** None (for most commands), or optional test path/parameters
- **Output:** Test results, formatting changes, linting issues, coverage percentage

**Steps (for `/test-format`):**
1. Run `pytest` with `--maxfail=1 -x` (stop on first failure)
2. If tests fail → summarize failures and STOP
3. If tests pass → run `black .` and `ruff check . --fix`
4. Generate coverage report with `--cov=backend/app --cov-report=term-missing`
5. Provide summary of results

**c. How to run it**

**Location:** `.claude/commands/` (repository root)

**Usage:** In Claude Code, simply type:
```
/test-format
```

**Expected Output:**
```
=== Running Tests ===
3 passed, 2 warnings, 2 errors in 0.17s

=== Formatting Code ===
reformatted backend/app/routers/notes.py
All done! ✨ 🍰 ✨

=== Linting ===
Found 2 errors (2 fixed, 0 remaining)

=== Coverage Report ===
Name                                  Stmts   Miss  Cover   Missing
-------------------------------------------------------------------
backend/app/models.py                    13      0   100%
backend/app/schemas.py                   18      0   100%
backend/app/routers/notes.py             30      4    87%
TOTAL                                   155     28    82%
```

**Rollback/Safety:**
- Tests run first with `-x` flag to stop on failures
- Formatting and linting only execute if tests pass
- Ruff `--fix` is safe and only fixes clear issues
- All changes are tracked via git, allowing easy rollback

**d. Before vs. after**

**Before (Manual Workflow):**
```bash
# Step 1: Run tests
cd week4 && python -m pytest backend/tests -q

# Step 2: Check if tests passed, then format
cd week4 && python -m black .

# Step 3: Fix linting issues
cd week4 && python -m ruff check . --fix

# Step 4: Run coverage
cd week4 && python -m pytest backend/tests --cov=backend/app

# Total: 4 separate commands, must check each step's output
```

**After (Automated Workflow):**
```bash
/test-format
# One command handles everything with intelligent flow control
```

**Time Saved:** ~2-3 minutes per iteration, reduced context switching, fewer mistakes.

**e. How you used the automation to enhance the starter application**

Used `/test-format` to:
1. Verify initial test suite (82% coverage baseline)
2. Automatically fix linting issues (e.g., `Optional[str]` → `str | None`)
3. Ensure code quality standards before adding new features
4. Streamlined the development loop when implementing features from `docs/TASKS.md`

The automation made it easy to maintain code quality throughout development, reducing the friction of running tests and formatting manually.


### Automation #2: CLAUDE.md Repository Guidance

**a. Design inspiration**

Based on [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices) recommendation: "Provide repository-specific instructions, context, or guidance that influence Claude's behavior" through CLAUDE.md files. The guide states: "Keep it concise and actionable" and "Document custom tools/scripts you expect Claude to use."

**b. Design of each automation**

**Goal:** Provide Claude Code with project-specific context, workflows, and safety guidelines to improve its assistance quality.

**Inputs/Outputs:**
- **Input:** Automatically read when starting a conversation in week4/
- **Output:** Better code suggestions, adherence to project patterns, safer command execution

**Key Sections:**
1. **Project Structure** - Complete directory overview with file descriptions
2. **Quick Start** - Commands for running, testing, and code quality
3. **Code Style Guidelines** - Python/FastAPI/Testing conventions
4. **Common Workflows** - Step-by-step guides for adding endpoints, models
5. **Safety Guidelines** - Safe vs. unsafe commands, pre-commit hooks
6. **API Documentation** - Current endpoints and usage
7. **Extension Tasks** - Reference to practice tasks

**c. How to run it**

**Location:** `week4/CLAUDE.md`

**Usage:** Automatically loaded when working in the week4/ directory. No manual invocation needed.

**Expected Behavior:**
When asking Claude to "add an endpoint for deleting notes," it will:
1. Write tests first in `backend/tests/test_notes.py`
2. Implement in `backend/app/routers/notes.py`
3. Follow existing patterns (HTTPException, get_db, etc.)
4. Use proper type hints and Pydantic schemas
5. Run tests and formatting before completion

**Rollback/Safety:**
The CLAUDE.md includes explicit safety guidelines:
- **Safe Commands:** `python -m pytest`, `python -m black`, `python -m ruff`
- **Commands to Avoid:** Direct pytest/black/ruff without `python -m`, manual DB edits
- **Pre-commit Hooks:** Enforced via `.pre-commit-config.yaml`

**d. Before vs. after**

**Before (Without CLAUDE.md):**
- Claude might suggest generic patterns not matching the codebase
- Could use unsafe commands or wrong file locations
- Would need repeated explanations of project structure
- Might not follow TDD approach required by the project

**After (With CLAUDE.md):**
- Claude automatically knows the project structure
- Follows established patterns (routers in `backend/app/routers/`, etc.)
- Uses safe commands with `python -m` prefix
- Writes tests first before implementation
- Suggests appropriate HTTP status codes and error handling

**Example improvement:**
```
User: "Add a DELETE endpoint for notes"

Without CLAUDE.md:
→ Claude might ask where to add it, what patterns to follow

With CLAUDE.md:
→ Claude knows to:
  1. Add tests to test_notes.py first
  2. Add route to routers/notes.py
  3. Return 204 on success, 404 if not found
  4. Run tests and formatting
```

**e. How you used the automation to enhance the starter application**

The CLAUDE.md file enhanced development by:

1. **Faster Onboarding:** When implementing features from `docs/TASKS.md`, Claude immediately understood:
   - Where to add new routes (`backend/app/routers/`)
   - How to structure schemas (`schemas.py`)
   - What testing patterns to follow (`conftest.py` fixtures)

2. **Consistent Code Quality:** Claude automatically:
   - Applied black formatting before suggesting changes
   - Used type hints and Pydantic schemas
   - Followed FastAPI patterns from the codebase

3. **Safer Operations:** The safety guidelines prevented:
   - Dangerous database operations
   - Wrong test execution methods
   - Missing pre-commit checks

4. **Workflow Automation:** Common workflows like "adding an endpoint" became single requests with Claude handling all steps correctly.

The CLAUDE.md transformed Claude from a generic assistant into a project-aware pair programmer that consistently follows the project's conventions and best practices.


### Automation #3: SubAgents (TestAgent + CodeAgent)

**a. Design inspiration**

Based on [SubAgents Documentation](https://code.claude.com/docs/en/sub-agents) which describes "specialized, autonomous assistants designed to execute specific, well-defined tasks." The documentation emphasizes using subagents for "role-specialized agents that run in isolated context windows" and "building your own AI development team where each member has specific expertise."

**b. Design of each automation**

**Goal:** Create a collaborative TDD workflow where specialized agents handle testing and implementation separately, mimicking a real development team.

**Agents Created:**
1. **TestAgent** (`.claude/agents/test-agent.md`) - QA specialist
2. **CodeAgent** (`.claude/agents/code-agent.md`) - Developer specialist

**Inputs/Outputs:**
- **Input:** Feature request (e.g., "Add DELETE endpoint for notes")
- **Output:** Tested, implemented, and documented feature

**Workflow:**
```
User Request
    ↓
TestAgent writes comprehensive tests
    ↓
Tests fail (Red) → Handoff to CodeAgent
    ↓
CodeAgent implements feature
    ↓
Tests pass (Green) → Handoff to TestAgent
    ↓
TestAgent verifies coverage and quality
    ↓
Feature Complete
```

**TestAgent Responsibilities:**
- Write tests first (TDD approach)
- Cover success, failure, and edge cases
- Aim for 80%+ coverage
- Verify tests pass after implementation

**CodeAgent Responsibilities:**
- Implement features to make tests pass
- Follow existing codebase patterns
- Maintain code quality (black, ruff)
- Use proper error handling and types

**c. How to run it**

**Location:**
- Agent configs: `.claude/agents/test-agent.md` and `code-agent.md`
- Orchestration: `.claude/commands/feature-dev.md` and `demo-subagents.md`

**Usage Options:**

1. **Full automation:**
```
/feature-dev Add DELETE /notes/{id} endpoint
```

2. **Demo mode:**
```
/demo-subagents
```

3. **Manual mode:**
```
User: "Act as TestAgent and write tests for DELETE endpoint"
[Claude reads test-agent.md and writes tests]

User: "/clear" then "Act as CodeAgent and implement DELETE endpoint"
[Claude reads code-agent.md and implements feature]

User: "/clear" then "Verify tests and coverage"
[Claude returns to TestAgent role and verifies]
```

**Expected Output:**
```
[TestAgent Phase]
→ Writing tests for DELETE /notes/{id}
→ Added 3 test cases: success, not found, database verification
→ Tests written. Ready for CodeAgent.

[CodeAgent Phase]
→ Implementing DELETE endpoint in routers/notes.py
→ Adding route: @router.delete("/{note_id}", status_code=204)
→ Using db.delete() and db.flush()
→ Running tests... ALL PASSING ✓
→ Formatting with black... DONE
→ Linting with ruff... CLEAN

[TestAgent Verification]
→ Full test suite: 5 passed
→ Coverage: 94% for notes.py
→ Feature complete!
```

**Rollback/Safety:**
- Each agent operates in isolated context (use `/clear` between phases)
- Tests written before code prevents breaking changes
- All changes tracked via git
- Safety guidelines inherited from CLAUDE.md

**d. Before vs. after**

**Before (Single Agent Workflow):**
```
User: "Add DELETE endpoint for notes"
→ Claude writes tests AND implementation together
→ Might skip edge cases in tests
→ Could miss testing scenarios
→ Less separation of concerns
→ Harder to review individual contributions
```

**After (SubAgent Workflow):**
```
User: "/feature-dev Add DELETE endpoint for notes"
→ TestAgent focuses solely on comprehensive testing
→ CodeAgent focuses solely on clean implementation
→ Clear handoff points with verification
→ Each agent follows their specialized guidelines
→ Better separation of concerns
→ Easier to review and iterate
```

**Key Improvements:**
- **Specialization:** Each agent has deep expertise in their domain
- **Accountability:** Clear handoff points for verification
- **Quality:** TestAgent ensures coverage, CodeAgent ensures patterns
- **Collaboration:** Mimics real team workflows

**e. How you used the automation to enhance the starter application**

The SubAgent automation enhanced development by:

1. **Better Test Coverage:**
   - TestAgent systematically covered success (200), validation (400), and not found (404) cases
   - Achieved 90%+ coverage on new features
   - Caught edge cases that might be missed in single-agent approach

2. **Cleaner Code:**
   - CodeAgent followed established patterns consistently
   - Proper use of Pydantic schemas and type hints
   - Error handling with appropriate HTTP status codes

3. **Faster Iteration:**
   - Clear workflow reduced back-and-forth
   - Each agent could work independently without context switching
   - Handoff points provided natural verification checkpoints

4. **Team Simulation:**
   - Demonstrated how specialized AI agents can collaborate
   - Provided a template for more complex multi-agent workflows
   - Showed the value of role specialization in AI-assisted development

5. **Scalability:**
   - Pattern can be extended with more agents (DocsAgent, DBAgent, etc.)
   - Each new agent can have specialized tools and knowledge
   - Workflow can be parallelized for independent tasks

The SubAgent approach transformed Claude from a single assistant into a coordinated team of specialists, each bringing deep expertise to their part of the development process.

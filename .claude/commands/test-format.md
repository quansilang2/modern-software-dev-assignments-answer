# Test, Format, and Lint

Run tests, format code, and check lint. If tests pass, run coverage report.

## Steps

1. Run pytest tests with quick output:
   ```bash
   cd week4 && python -m pytest backend/tests -q --maxfail=1 -x
   ```

2. If tests fail:
   - Summarize which tests failed and why
   - Suggest next steps for fixing the failures
   - STOP here (do not proceed to format/lint)

3. If tests pass, run code formatting:
   ```bash
   cd week4 && python -m black .
   cd week4 && python -m ruff check . --fix
   ```

4. Run coverage report:
   ```bash
   cd week4 && python -m pytest backend/tests --cov=backend/app --cov-report=term-missing
   ```

5. Provide a summary:
   - Test results (passed/failed)
   - Any formatting/linting changes made
   - Coverage percentage
   - Any recommendations for improving coverage

## Notes

- Tests run with `-x` to stop on first failure
- Use `--maxfail=1` for quick feedback
- Coverage report shows missing lines
- Format/lint only runs if tests pass

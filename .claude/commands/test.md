# Run Tests

Run pytest tests. Optional: pass path or marker as $ARGUMENTS.

## Command

```bash
cd week4 && python -m pytest backend/tests $ARGUMENTS -v
```

## If no arguments provided

Run all tests with verbose output:
```bash
cd week4 && python -m pytest backend/tests -v
```

## If arguments provided

Example usage:
- `/test backend/tests/test_notes.py` - Run specific test file
- `/test -k "create"` - Run tests matching "create"
- `/test -x` - Stop on first failure
- `/test --maxfail=3` - Stop after 3 failures

## Notes

- Use `-v` for verbose output to see test names
- Use `-s` to see print statements
- Use `-x` to stop on first failure
- Use `--tb=short` for shorter tracebacks

# print_summary

**Class:** `SafeLoader`

Print a formatted summary report of all operations.

## Signature

```python
def print_summary()
```

## Parameters

None

## Returns

None (prints to console)

## Example

```python
from py_safe_loader import SafeLoader

loader = SafeLoader()

# Perform operations
loader.load_modules(['os', 'sys', 'requests', 'fake_module'])

def test_function():
    return "Success!"

loader.safe_execute(test_function)

def failing_function():
    raise ValueError("This fails")

loader.safe_execute(failing_function)

# Print formatted summary
loader.print_summary()
```

## Sample Output

```
============================================================
SAFELOADER SUMMARY REPORT
============================================================
Total Modules Attempted: 4
Successfully Loaded: 3
Failed to Load: 1

✓ Loaded Modules:
  - os
  - sys
  - requests

✗ Failed Modules:
  - fake_module: Import error: No module named 'fake_module'

Execution History (2 operations):
  ✓ test_function - 10:30:20
  ✗ failing_function - 10:30:21
    Error: ValueError: This fails
============================================================
```

## Use With Context Manager

```python
with SafeLoader(verbose=True) as loader:
    loader.load_modules(['os', 'sys', 'fake_module'])
    
    def my_func():
        return 42
    
    loader.safe_execute(my_func)

# Summary is automatically printed when context exits
```

## Notes

- Provides a clean, formatted overview of all operations
- Shows both successful and failed operations
- Includes execution history with timestamps
- Automatically called when using SafeLoader as a context manager
- Use `get_summary()` if you need the raw data instead

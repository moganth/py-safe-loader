# get_summary

**Class:** `SafeLoader`

Get statistics and details of all operations performed.

## Signature

```python
def get_summary() -> Dict
```

## Parameters

None

## Returns

Dictionary containing:
- **total_attempted** (int): Total modules attempted to load
- **successful** (int): Number of successfully loaded modules
- **failed** (int): Number of failed module loads
- **loaded_modules** (List[str]): List of successfully loaded module names
- **failed_modules** (Dict[str, str]): Dictionary mapping failed module names to error messages
- **execution_history** (List[Dict]): List of all safe_execute operations with status and timestamp

## Example

```python
from py_safe_loader import SafeLoader

loader = SafeLoader()

# Perform various operations
loader.load_modules(['os', 'sys', 'fake_module'])

def test_func():
    return 42

loader.safe_execute(test_func)

def failing_func():
    raise ValueError("Test error")

loader.safe_execute(failing_func)

# Get summary
summary = loader.get_summary()

print(f"Total modules attempted: {summary['total_attempted']}")
print(f"Successful: {summary['successful']}")
print(f"Failed: {summary['failed']}")
print(f"Loaded modules: {summary['loaded_modules']}")
print(f"Failed modules: {summary['failed_modules']}")
print(f"Execution history: {summary['execution_history']}")
```

## Sample Output

```python
{
    'total_attempted': 3,
    'successful': 2,
    'failed': 1,
    'loaded_modules': ['os', 'sys'],
    'failed_modules': {
        'fake_module': "Import error: No module named 'fake_module'"
    },
    'execution_history': [
        {
            'function': 'test_func',
            'status': 'success',
            'timestamp': '10:30:20'
        },
        {
            'function': 'failing_func',
            'status': 'failed',
            'error': 'ValueError: Test error',
            'timestamp': '10:30:21'
        }
    ]
}
```

## Use Cases

- Debugging: See what failed and why
- Logging: Export summary to logs
- Monitoring: Track application health
- Testing: Verify expected operations occurred
- Reporting: Generate reports of module availability

## Notes

- Summary includes all operations since loader creation or last reset
- Use with `print_summary()` for formatted output
- Call `reset()` to clear tracking data and start fresh

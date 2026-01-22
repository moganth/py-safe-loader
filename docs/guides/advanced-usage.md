# Advanced Usage Guide

## Safe Code Execution

### Execute Code Strings

```python
loader = SafeLoader()

# Execute code string
code = """
def greet(name):
    return f"Hello, {name}!"

result = greet("SafeLoader")
"""

success, namespace, error = loader.safe_exec_code(code)

if success:
    print(namespace['result'])  # Access variables from executed code
```

### Execute Python Files

```python
loader = SafeLoader()

# Execute a Python file safely
success, namespace, error = loader.safe_exec_file('script.py')

if success:
    # Access functions and variables from the executed file
    if 'my_function' in namespace:
        namespace['my_function']()
```

## Import with Install Suggestions

```python
loader = SafeLoader()

# Try to import, get helpful message if not installed
requests = loader.try_import_or_install('requests')
pandas = loader.try_import_or_install('pandas')

if requests:
    print("Requests is available!")
else:
    print("Install suggestion shown in console")
```

## Error Logging to File

```python
# All operations will be logged to file
loader = SafeLoader(verbose=True, log_file='app_errors.log')

loader.load_modules(['os', 'fake_module'])

def failing_function():
    raise ValueError("Test error")

loader.safe_execute(failing_function)

# Check 'app_errors.log' for detailed logs
```

## Summary Reports

```python
loader = SafeLoader()

# Perform various operations
loader.load_modules(['os', 'sys', 'fake_module'])

def test_func():
    return 42

loader.safe_execute(test_func)

# Get summary dictionary
summary = loader.get_summary()
print(summary)

# Or print formatted summary
loader.print_summary()
```

## Context Manager Pattern

The recommended way to use SafeLoader is with Python's context manager:

```python
from py_safe_loader import SafeLoader

with SafeLoader(verbose=True, log_file='errors.log') as loader:
    # Load modules
    modules = loader.load_modules(['os', 'sys', 'requests'])
    
    # Execute functions safely
    def my_function():
        return "Hello, World!"
    
    success, result, error = loader.safe_execute(my_function)

# Automatic summary report and cleanup at context exit
```

## See Also

- [Real-World Examples](../examples/)
- [Function Reference](../reference/SafeLoader.md)

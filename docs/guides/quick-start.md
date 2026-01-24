# Quick Start Guide

## Basic Module Loading

```python
from py_safe_loader import SafeLoader

# Create loader instance
loader = SafeLoader(verbose=True)

# Load modules - missing modules won't crash your program!
modules = loader.load_modules([
    'os',
    'sys',
    'requests',         # Works if installed
    'fake_module',      # Fails gracefully - program continues
    'pandas'
])

# Use loaded modules
if 'os' in modules:
    print(modules['os'].getcwd())
```

## One-Liner Quick Load

```python
from py_safe_loader import quick_load

# Load modules with a single function call
modules = quick_load('os', 'sys', 'json', 'non_existent_module')
```

## Safe Function Execution

```python
from py_safe_loader import SafeLoader

loader = SafeLoader()

def risky_function(a, b):
    return a / b  # Might cause division by zero

# Execute safely - returns (success, result, error)
success, result, error = loader.safe_execute(risky_function, 10, 0)

if success:
    print(f"Result: {result}")
else:
    print(f"Error caught: {error}")
    # Your program continues running!
```

## Quick Safe Run

```python
from py_safe_loader import safe_run

# Quick one-liner for safe function execution
success, result, error = safe_run(lambda: 5 * 5)
```

## Context Manager (Recommended)

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

## Next Steps

- Check out the [Advanced Usage](./advanced-usage.md) guide
- Explore [Real-World Examples](../examples/)
- Read the [Function Reference](../reference/SafeLoader.md)

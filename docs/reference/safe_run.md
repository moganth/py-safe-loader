# safe_run

**Type:** Convenience Function (not a class method)

Quick function to safely execute any function without creating a SafeLoader instance.

## Signature

```python
def safe_run(func: Callable, *args, **kwargs) -> tuple
```

## Parameters

- **func** (Callable): The function to execute
- ***args**: Positional arguments to pass to the function
- ****kwargs**: Keyword arguments to pass to the function

## Returns

Tuple of `(success, result, error)`:
- **success** (bool): `True` if function executed without errors
- **result** (Any): Return value if successful, `None` otherwise
- **error** (str): Error message if failed, `None` otherwise

## Examples

### Basic Usage

```python
from py_safe_loader import safe_run

# Quick one-liner for safe execution
success, result, error = safe_run(lambda: 5 * 5)

if success:
    print(result)  # Output: 25
```

### With Arguments

```python
def divide(a, b):
    return a / b

# Safe division
success, result, error = safe_run(divide, 10, 2)
print(result)  # Output: 5.0

# Safe division by zero - no crash!
success, result, error = safe_run(divide, 10, 0)
if not success:
    print(f"Error: {error}")  # Error caught, program continues
```

### Error Handling Pattern

```python
def risky_operation(data):
    # Some operation that might fail
    return process_complex_data(data)

success, result, error = safe_run(risky_operation, my_data)

if success:
    print(f"Success: {result}")
else:
    print(f"Operation failed: {error}")
    # Fallback logic here
    result = use_cached_data()
```

### With Keyword Arguments

```python
def greet(name, greeting="Hello", punctuation="!"):
    return f"{greeting}, {name}{punctuation}"

success, result, error = safe_run(
    greet, 
    "World", 
    greeting="Hi",
    punctuation="!!!"
)

print(result)  # Output: Hi, World!!!
```

### Quick Testing

```python
# Test multiple functions quickly
functions = [
    (lambda: 1/1, "Division 1/1"),
    (lambda: 1/0, "Division 1/0"),
    (lambda: int("123"), "Parse valid int"),
    (lambda: int("abc"), "Parse invalid int"),
]

for func, description in functions:
    success, result, error = safe_run(func)
    status = "✓" if success else "✗"
    print(f"{status} {description}: {result if success else error}")
```

Output:
```
✓ Division 1/1: 1.0
✗ Division 1/0: division by zero
✓ Parse valid int: 123
✗ Parse invalid int: invalid literal for int()
```

## Comparison with SafeLoader

### Using safe_run (one-liner):
```python
success, result, error = safe_run(my_function, arg1, arg2)
```

### Using SafeLoader (more control):
```python
loader = SafeLoader(verbose=True, log_file='errors.log')
success, result, error = loader.safe_execute(my_function, arg1, arg2)
loader.print_summary()
```

## When to Use

**Use `safe_run` when:**
- You need a quick one-liner
- You're testing a single function
- You don't need execution tracking
- You don't need logging

**Use `SafeLoader.safe_execute()` when:**
- You need execution history
- You want detailed logging
- You need summary reports
- You're executing multiple operations

## Notes

- Creates a temporary SafeLoader instance internally
- No execution tracking or logging
- Perfect for quick tests and simple scripts
- Never raises exceptions - always returns tuple

# safe_execute

**Class:** `SafeLoader`

Execute any function safely with automatic error catching.

## Signature

```python
def safe_execute(func: Callable, *args, **kwargs) -> tuple
```

## Parameters

- **func** (Callable): The function to execute
- ***args**: Positional arguments to pass to the function
- ****kwargs**: Keyword arguments to pass to the function

## Returns

Tuple of `(success, result, error)`:
- **success** (bool): `True` if function executed without errors, `False` otherwise
- **result** (Any): Return value of the function if successful, `None` otherwise
- **error** (str): Error message if failed, `None` otherwise

## Examples

### Basic Usage

```python
from py_safe_loader import SafeLoader

loader = SafeLoader()

def risky_function(a, b):
    return a / b

# Execute safely
success, result, error = loader.safe_execute(risky_function, 10, 2)

if success:
    print(f"Result: {result}")  # Output: Result: 5.0
else:
    print(f"Error: {error}")
```

### Handling Errors

```python
# This won't crash your program
success, result, error = loader.safe_execute(risky_function, 10, 0)

if success:
    print(f"Result: {result}")
else:
    print(f"Division by zero caught: {error}")
    # Your program continues running!
```

### With Lambda Functions

```python
success, result, error = loader.safe_execute(lambda x: x ** 2, 5)
print(result)  # Output: 25
```

### With Arguments

```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

success, result, error = loader.safe_execute(greet, "World", greeting="Hi")
print(result)  # Output: Hi, World!
```

## Notes

- Never raises exceptions - always returns a tuple
- All exceptions are caught and returned as error messages
- Execution is tracked in history
- Ideal for executing untrusted or experimental code

# safe_exec_code

**Class:** `SafeLoader`

Execute Python code from a string safely using exec().

## Signature

```python
def safe_exec_code(code: str, namespace: dict = None) -> tuple
```

## Parameters

- **code** (str): Python code string to execute
- **namespace** (dict, optional): Namespace dictionary for execution. Default: `None` (creates new namespace)

## Returns

Tuple of `(success, namespace, error)`:
- **success** (bool): `True` if code executed without errors
- **namespace** (dict): Dictionary containing all variables/functions from executed code
- **error** (str): Error message if failed, `None` otherwise

## Examples

### Basic Code Execution

```python
from py_safe_loader import SafeLoader

loader = SafeLoader()

code = """
def greet(name):
    return f"Hello, {name}!"

result = greet("SafeLoader")
"""

success, namespace, error = loader.safe_exec_code(code)

if success:
    print(namespace['result'])  # Output: Hello, SafeLoader!
    print(namespace['greet']("World"))  # Output: Hello, World!
```

### With Custom Namespace

```python
# Provide initial namespace
custom_ns = {'x': 10, 'y': 20}

code = """
z = x + y
result = z * 2
"""

success, namespace, error = loader.safe_exec_code(code, custom_ns)

if success:
    print(namespace['z'])  # Output: 30
    print(namespace['result'])  # Output: 60
```

### Error Handling

```python
bad_code = """
def divide(a, b):
    return a / b

result = divide(10, 0)  # Division by zero!
"""

success, namespace, error = loader.safe_exec_code(bad_code)

if not success:
    print(f"Error caught: {error}")
    # Program continues running
```

### Multi-line Scripts

```python
code = """
import math

def calculate_circle(radius):
    area = math.pi * radius ** 2
    circumference = 2 * math.pi * radius
    return area, circumference

area, circ = calculate_circle(5)
"""

success, namespace, error = loader.safe_exec_code(code)

if success:
    print(f"Area: {namespace['area']}")
    print(f"Circumference: {namespace['circ']}")
```

## Notes

- Code is executed in an isolated namespace
- All variables and functions from executed code are accessible via returned namespace
- Errors don't crash the program - they're returned as strings
- Useful for dynamic code execution, plugin systems, or testing code snippets

# safe_exec_file

**Class:** `SafeLoader`

Execute a Python file safely.

## Signature

```python
def safe_exec_file(file_path: str, namespace: dict = None) -> tuple
```

## Parameters

- **file_path** (str): Path to the Python file to execute
- **namespace** (dict, optional): Namespace dictionary for execution. Default: `None`

## Returns

Tuple of `(success, namespace, error)`:
- **success** (bool): `True` if file executed without errors
- **namespace** (dict): Dictionary containing all variables/functions from executed file
- **error** (str): Error message if failed, `None` otherwise

## Examples

### Basic File Execution

```python
from py_safe_loader import SafeLoader

loader = SafeLoader()

# Execute a Python file
success, namespace, error = loader.safe_exec_file('script.py')

if success:
    # Access functions from the executed file
    if 'my_function' in namespace:
        result = namespace['my_function']()
        print(result)
```

### Accessing File Variables

Suppose `config.py` contains:

```python
# config.py
DATABASE_URL = "postgresql://localhost/mydb"
API_KEY = "secret123"
DEBUG = True

def get_config():
    return {
        'db': DATABASE_URL,
        'key': API_KEY,
        'debug': DEBUG
    }
```

You can safely execute and access it:

```python
success, namespace, error = loader.safe_exec_file('config.py')

if success:
    print(namespace['DATABASE_URL'])
    print(namespace['DEBUG'])
    config = namespace['get_config']()
```

### Error Handling

```python
# Try to execute a file that might have errors
success, namespace, error = loader.safe_exec_file('risky_script.py')

if not success:
    print(f"Script execution failed: {error}")
    # Your program continues running
else:
    print("Script executed successfully")
```

### With Custom Namespace

```python
# Provide variables to the script
custom_ns = {
    'input_data': [1, 2, 3, 4, 5],
    'multiplier': 10
}

success, namespace, error = loader.safe_exec_file('process.py', custom_ns)

if success:
    print(namespace['output_data'])
```

## Notes

- File is read and executed safely
- All functions, classes, and variables from the file are accessible
- File reading errors and execution errors are both caught
- Useful for plugin systems, dynamic script loading, or configuration files
- The file path can be absolute or relative

# SafeLoader Class

The main class for safe module loading and code execution.

## Constructor

```python
SafeLoader(verbose=True, log_file=None)
```

### Parameters
- **verbose** (bool): Print detailed messages. Default: `True`
- **log_file** (str, optional): File path to log errors. Default: `None`

### Example
```python
from py_safe_loader import SafeLoader

# Create loader with verbose output
loader = SafeLoader(verbose=True)

# Create loader with file logging
loader = SafeLoader(verbose=True, log_file='errors.log')

# Use as context manager (recommended)
with SafeLoader(verbose=True, log_file='app.log') as loader:
    # Your code here
    pass
```

## Methods

The SafeLoader class provides the following methods:

- [load_module](./load_module.md) - Load a single module safely
- [load_modules](./load_modules.md) - Load multiple modules
- [safe_execute](./safe_execute.md) - Execute a function safely
- [safe_exec_code](./safe_exec_code.md) - Execute code string safely
- [safe_exec_file](./safe_exec_file.md) - Execute Python file safely
- [try_import_or_install](./try_import_or_install.md) - Import with installation suggestions
- [get_summary](./get_summary.md) - Get operation statistics
- [print_summary](./print_summary.md) - Print formatted summary report
- [reset](./reset.md) - Clear all tracking data

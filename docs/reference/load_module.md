# load_module

**Class:** `SafeLoader`

Load a single module safely without crashing your program.

## Signature

```python
def load_module(module_name: str) -> Optional[Any]
```

## Parameters

- **module_name** (str): Name of the module to import

## Returns

- Module object if successful
- `None` if import fails

## Example

```python
from py_safe_loader import SafeLoader

loader = SafeLoader(verbose=True)

# Load a module
os_module = loader.load_module('os')

if os_module:
    print(os_module.getcwd())
else:
    print("Failed to load os module")

# Try to load non-existent module - returns None, doesn't crash
fake_module = loader.load_module('fake_module')
print(f"Fake module loaded: {fake_module}")  # Output: None
```

## Notes

- Missing modules return `None` instead of raising ImportError
- Error details are logged if `verbose=True` or `log_file` is set
- All operations are tracked in execution history

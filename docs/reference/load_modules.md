# load_modules

**Class:** `SafeLoader`

Load multiple modules at once safely.

## Signature

```python
def load_modules(module_names: List[str]) -> Dict[str, Any]
```

## Parameters

- **module_names** (List[str]): List of module names to import

## Returns

- Dictionary mapping module names to module objects
- Only successfully loaded modules are included in the dictionary

## Example

```python
from py_safe_loader import SafeLoader

loader = SafeLoader(verbose=True)

# Load multiple modules
modules = loader.load_modules([
    'os',
    'sys',
    'json',
    'requests',         # Works if installed
    'fake_module',      # Fails gracefully
    'pandas'
])

# Use loaded modules
if 'os' in modules:
    print(modules['os'].getcwd())

if 'requests' in modules:
    response = modules['requests'].get('https://example.com')

# Check what failed
loader.print_summary()
```

## Output Example

```
[2026-01-22 10:30:15] [INFO] Loading 4 modules...
[2026-01-22 10:30:15] [SUCCESS] ✓ Successfully loaded module: os
[2026-01-22 10:30:15] [SUCCESS] ✓ Successfully loaded module: sys
[2026-01-22 10:30:15] [ERROR] ✗ Failed to load fake_module: Import error
[2026-01-22 10:30:15] [SUCCESS] ✓ Successfully loaded module: json
[2026-01-22 10:30:15] [INFO] Loaded 3/4 modules successfully
```

## Notes

- Failed modules are skipped, not included in return dictionary
- All operations are logged and tracked
- Program continues even if some modules fail to load

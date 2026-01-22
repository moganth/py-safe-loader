# quick_load

**Type:** Convenience Function (not a class method)

Quick function to load modules without creating a SafeLoader instance.

## Signature

```python
def quick_load(*module_names, verbose=True) -> Dict[str, Any]
```

## Parameters

- ***module_names** (str): Variable number of module names to load
- **verbose** (bool, optional): Print detailed messages. Default: `True`

## Returns

Dictionary mapping module names to module objects (only successful loads)

## Examples

### Basic Usage

```python
from py_safe_loader import quick_load

# Load modules with one line
modules = quick_load('os', 'sys', 'json', 'fake_module')

# Use loaded modules
if 'os' in modules:
    print(modules['os'].getcwd())

if 'json' in modules:
    data = modules['json'].dumps({'key': 'value'})
```

### Without Verbose Output

```python
# Silent loading
modules = quick_load('os', 'sys', 'json', verbose=False)
```

### Conditional Feature Loading

```python
# Try to load optional dependencies
modules = quick_load('requests', 'pandas', 'matplotlib', 'seaborn')

if 'requests' in modules:
    # Use requests for API calls
    response = modules['requests'].get('https://api.example.com')

if 'pandas' in modules:
    # Use pandas for data processing
    df = modules['pandas'].DataFrame({'a': [1, 2, 3]})

if 'matplotlib' not in modules:
    print("Matplotlib not available - skipping plots")
```

### Quick Script Setup

```python
from py_safe_loader import quick_load

# One-liner to setup all dependencies
m = quick_load('os', 'sys', 'json', 'pathlib', 'datetime')

# Use with short variable name
current_time = m['datetime'].datetime.now()
current_dir = m['pathlib'].Path.cwd()
```

## Comparison with SafeLoader

### Using quick_load (one-liner):
```python
modules = quick_load('os', 'sys', 'json')
```

### Using SafeLoader (more control):
```python
loader = SafeLoader(verbose=True, log_file='errors.log')
modules = loader.load_modules(['os', 'sys', 'json'])
loader.print_summary()
```

## When to Use

**Use `quick_load` when:**
- You need a quick one-liner
- You don't need execution tracking
- You don't need to execute functions safely
- You just want to load modules

**Use `SafeLoader` when:**
- You need execution history
- You want to use `safe_execute()`
- You need file logging
- You want summary reports
- You're building a larger application

## Notes

- Creates a temporary SafeLoader instance internally
- No access to execution tracking or safe_execute
- Perfect for simple scripts and quick tasks
- Returns only successfully loaded modules

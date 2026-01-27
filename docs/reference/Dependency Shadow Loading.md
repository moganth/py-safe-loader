# Dependency Shadow Loading with Automatic Fallback

## Overview

**Shadow Loading** is a feature that enables safe dependency updates by automatically testing code with newer versions and falling back to stable versions if the update breaks functionality.

## Problem It Solves

When updating dependencies to newer major versions, there's always a risk of breaking changes. Traditional approaches require:
1. Manual testing after each update
2. Reverting changes if something breaks
3. Time-consuming diagnosis of compatibility issues

**Shadow Loading** automates this process by:
- **Attempting** to load and run code with updated versions
- **Testing** if the code still works correctly
- **Automatically falling back** to stable versions if something breaks
- **Logging** all attempts for debugging and analysis

## How It Works

```
                    ┌─────────────────────┐
                    │  Start with STABLE  │
                    │   Version Running   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Try UPDATED        │
                    │  Version (e.g. v2)  │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
                    ▼                     ▼
            ✅ Works?            ❌ Breaks?
                    │                     │
                    ▼                     ▼
            ✓ Update            🔄 Fallback to
            Successful           Stable Version
                                      │
                                      ▼
                                ✓ Roll Back
                                Complete
```

## API Reference

### `shadow_load_with_fallback()`

```python
loader.shadow_load_with_fallback(
    test_func: Callable,
    updated_packages: Dict[str, str],
    stable_packages: Optional[Dict[str, str]] = None,
    test_args: tuple = (),
    test_kwargs: Optional[Dict] = None
) -> Dict[str, Any]
```

#### Parameters

- **`test_func`** (Callable): Function that tests your code. Should exercise the functionality that depends on the updated packages.
- **`updated_packages`** (Dict): Package versions to test. Example: `{"numpy": "2.0.0", "pandas": "2.1.0"}`
- **`stable_packages`** (Optional[Dict]): Fallback versions if test fails. If None, no fallback is attempted.
- **`test_args`** (tuple): Positional arguments to pass to `test_func`
- **`test_kwargs`** (Dict): Keyword arguments to pass to `test_func`

#### Returns

Dictionary containing:

```python
{
    "success": bool,              # True if test passed with updated versions
    "active_versions": Dict,      # Current installed versions
    "tested_with": Dict,          # Versions that were tested
    "fallback_used": bool,        # True if fallback was triggered
    "fallback_to": Dict,          # Versions used for fallback
    "test_result": Tuple,         # (success, result, error) from test execution
    "message": str,               # Human-readable status message
    "log_entries": List           # Detailed log of all operations
}
```

## Usage Examples

### Example 1: Simple Dependency Update

```python
from safe_loader import SafeLoader

loader = SafeLoader()

def test_my_code():
    """Test function that exercises dependent code"""
    import numpy as np
    import pandas as pd
    
    # Your actual working code
    data = np.array([1, 2, 3, 4, 5])
    df = pd.DataFrame({'values': data})
    return df.sum().sum()

# Try updating to newer versions
result = loader.shadow_load_with_fallback(
    test_func=test_my_code,
    updated_packages={"numpy": "2.0.0", "pandas": "2.1.0"},
    stable_packages={"numpy": "1.26.0", "pandas": "1.5.0"}
)

if result['success']:
    print("✓ Update successful! Code works with new versions.")
else:
    print("⚠ Update failed. Rolled back to stable versions.")
    print(f"Reason: {result['message']}")
```

### Example 2: Gradual Version Adoption

```python
# Test each major version step-by-step
def test_dataframe_operations():
    import pandas as pd
    df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    return df.groupby('A').sum()

# First try 2.0
result_v2 = loader.shadow_load_with_fallback(
    test_func=test_dataframe_operations,
    updated_packages={"pandas": "2.0.0"},
    stable_packages={"pandas": "1.5.0"}
)

if result_v2['success']:
    # Try 2.1
    result_v2_1 = loader.shadow_load_with_fallback(
        test_func=test_dataframe_operations,
        updated_packages={"pandas": "2.1.0"},
        stable_packages={"pandas": "2.0.0"}
    )
```

### Example 3: Multiple Package Update

```python
def test_data_processing():
    """Complex code using multiple interdependent packages"""
    import numpy as np
    import scipy as sp
    import pandas as pd
    
    # Multi-package functionality
    matrix = np.random.rand(5, 5)
    eigenvalues = np.linalg.eigvals(matrix)
    
    series = pd.Series(eigenvalues)
    return series.describe()

result = loader.shadow_load_with_fallback(
    test_func=test_data_processing,
    updated_packages={
        "numpy": "2.0.0",
        "scipy": "1.12.0",
        "pandas": "2.1.0"
    },
    stable_packages={
        "numpy": "1.24.0",
        "scipy": "1.10.0",
        "pandas": "1.5.0"
    }
)

print(f"\nUpdate Status: {result['message']}")
print(f"Versions after test: {result['active_versions']}")
print(f"Fallback triggered: {result['fallback_used']}")
```

## Real-World Use Cases

### 1. **Continuous Integration Pipeline**
```python
# In CI/CD, automatically test if updates break your tests
def run_unit_tests():
    import subprocess
    result = subprocess.run(['pytest', 'tests/'], capture_output=True)
    if result.returncode != 0:
        raise RuntimeError("Tests failed")
    return True

shadow_load_with_fallback(
    test_func=run_unit_tests,
    updated_packages={"pytest-plugins": "latest"},
    stable_packages={"pytest-plugins": "current"}
)
```

### 2. **Critical Production Services**
```python
# Before deploying updates, verify compatibility
def critical_business_logic():
    # Your actual production code
    from vendor_lib import ProcessPayment
    result = ProcessPayment(amount=100)
    return result.success

result = shadow_load_with_fallback(
    test_func=critical_business_logic,
    updated_packages={"vendor-lib": "2.5.0"},
    stable_packages={"vendor-lib": "2.4.2"}
)

if result['success']:
    # Safe to deploy
    deploy_to_production()
```

### 3. **Long-Running Data Processing**
```python
def process_large_dataset():
    import pandas as pd
    df = pd.read_csv('large_data.csv')
    return df.groupby('category').agg({'value': 'sum'})

result = shadow_load_with_fallback(
    test_func=process_large_dataset,
    updated_packages={"pandas": "2.0.0"},
    stable_packages={"pandas": "1.5.0"}
)
```

## Important Notes

1. **Test Function Must Be Comprehensive**: Your `test_func` should exercise all critical code paths that depend on the updated packages.

2. **Logging**: All shadow loading attempts are logged. Enable `verbose=True` for detailed diagnostics.

3. **No Automatic Installation**: This feature assumes packages are already installed or will be installed separately. It only tests with what's available.

4. **Fallback Strategy**: If fallback fails, your system returns to the most stable known version logged in the results.

5. **Production Safety**: Always use shadow loading as part of automated testing before production deployments.

## Integration with SafeLoader

Shadow loading works seamlessly with other SafeLoader features:

```python
loader = SafeLoader(verbose=True, log_file='dependency-tests.log')

# Use shadow loading
result = loader.shadow_load_with_fallback(...)

# Check execution history
print(loader.execution_history)

# Get detailed logs
with open('dependency-tests.log', 'r') as f:
    print(f.read())
```

## Troubleshooting

### Issue: Fallback Doesn't Work
**Solution**: Ensure `stable_packages` contains the exact version strings that worked previously.

### Issue: Test Function Itself Has Errors
**Solution**: Test your `test_func` in isolation first to ensure it works correctly.

### Issue: Need to Test Without Fallback
**Solution**: Set `stable_packages=None` to only test with updated versions.

## See Also
- [SafeLoader API Documentation](./SafeLoader.md)
- [Dependency Version Checker](./Dependency_Version_Checker.md)
- [Advanced Usage Guide](../guides/advanced-usage.md)



# ShadowLoader - Multi-Version Dependency Management

## Overview

**ShadowLoader** is an advanced dependency management system that enables safe, automatic version switching and fallback for libraries. It allows you to load and test multiple versions of the same dependency simultaneously, with automatic switching to a working version if errors occur.

## Key Features

✅ **Multi-Version Loading** - Load multiple versions of the same package  
✅ **Automatic Fallback** - Switch to working version on errors  
✅ **Version Tracking** - Monitor which versions are loaded and active  
✅ **Real-Time Logging** - Timestamped logging with status indicators  
✅ **Execution History** - Track all version attempts and results  
✅ **Summary Reports** - Get detailed statistics and status overview  

## API Reference

### Constructor

```python
loader = ShadowLoader(verbose=True, log_file=None)
```

**Parameters:**
- `verbose` (bool): Enable console logging. Default: True
- `log_file` (str): Optional file path for logging output

### Methods

#### `add_shadow_versions(package, versions)`

Add multiple versions of a package to shadow load.

```python
loader.add_shadow_versions("requests", ["2.31.0", "2.28.2", "2.25.1"])
```

**Parameters:**
- `package` (str): Package name
- `versions` (List[str]): List of version strings to load

**Returns:** None

---

#### `get_active_version(package)`

Get the currently active version for a package.

```python
active = loader.get_active_version("requests")  # Returns "2.31.0"
```

**Parameters:**
- `package` (str): Package name

**Returns:** str or None - Currently active version

---

#### `switch_version(package, version)`

Manually switch to a different loaded version.

```python
loader.switch_version("requests", "2.25.1")
```

**Parameters:**
- `package` (str): Package name
- `version` (str): Target version

**Returns:** bool - True if switch successful

---

#### `execute_with_fallback(func, args=(), kwargs=None, package=None)`

Execute a function with automatic version fallback.

```python
def my_operation():
    import requests
    return requests.get("https://example.com")

success, result, error = loader.execute_with_fallback(
    my_operation,
    package="requests"
)
```

**Parameters:**
- `func` (Callable): Function to execute
- `args` (tuple): Positional arguments to pass to func
- `kwargs` (dict): Keyword arguments to pass to func
- `package` (str): Package to try versions for (optional)

**Returns:** tuple - (success: bool, result: Any, error: str)

---

#### `print_summary()`

Print a formatted summary report of all loaded versions.

```python
loader.print_summary()
```

**Output:**
```
======================================================================
SHADOW LOADER SUMMARY
======================================================================
Total Versions: 3
Loaded: 3
Failed: 0

Package: requests
   [OK] 2.31.0 [ACTIVE]
   [OK] 2.28.2
   [OK] 2.25.1

Execution History (last 5):
   [OK] requests==2.31.0 - 18:00:47

======================================================================
```

---

#### `get_summary_stats()`

Get summary statistics as a dictionary.

```python
stats = loader.get_summary_stats()
# Returns:
# {
#     'total_versions': 3,
#     'loaded': 3,
#     'failed': 0,
#     'packages': {'requests': ['2.31.0', '2.28.2', '2.25.1']},
#     'active_versions': {'requests': '2.31.0'},
#     'execution_count': 5
# }
```

**Returns:** dict - Statistics dictionary

## Usage Examples

### Example 1: Basic Multi-Version Loading

```python
from safe_loader import ShadowLoader

loader = ShadowLoader(verbose=True)

# Load multiple versions
loader.add_shadow_versions("requests", ["2.31.0", "2.28.2", "2.25.1"])

# Check active version
print(f"Active: {loader.get_active_version('requests')}")

# Print summary
loader.print_summary()
```

**Output:**
```
[2026-01-27 18:00:00] [i] [INFO] ShadowLoader initialized
[2026-01-27 18:00:00] [i] [INFO] Adding shadow versions for requests: ['2.31.0', '2.28.2', '2.25.1']
[2026-01-27 18:00:00] [OK] [SUCCESS] [OK] Loaded requests==2.31.0 (isolated)
[2026-01-27 18:00:00] [OK] [SUCCESS] [OK] Loaded requests==2.28.2 (isolated)
[2026-01-27 18:00:00] [OK] [SUCCESS] [OK] Loaded requests==2.25.1 (isolated)
[2026-01-27 18:00:00] [OK] [SUCCESS] [OK] Active version for requests: 2.31.0

Active: 2.31.0
```

---

### Example 2: Automatic Version Fallback

```python
def http_request():
    import requests
    return requests.get("https://api.example.com/data")

# Execute with automatic fallback across versions
success, result, error = loader.execute_with_fallback(
    http_request,
    package="requests"
)

if success:
    print(f"Success using {loader.get_active_version('requests')}")
else:
    print(f"All versions failed: {error}")
```

**Output:**
```
[2026-01-27 18:00:00] [i] [INFO] Trying requests==2.31.0...
[2026-01-27 18:00:00] [OK] [SUCCESS] [OK] Success with requests==2.31.0
Success using 2.31.0
```

---

### Example 3: Real-World API Compatibility

```python
def fetch_user_data(user_id):
    import requests
    response = requests.get(f"https://api.example.com/users/{user_id}")
    return response.json()

# Test compatibility with multiple versions
for version in ["3.0.0", "2.31.0", "2.28.2"]:
    loader.add_shadow_versions("requests", [version])
    
    success, data, error = loader.execute_with_fallback(
        lambda: fetch_user_data(123),
        package="requests"
    )
    
    if success:
        print(f"[OK] Version {version} works")
        break
    else:
        print(f"[FAIL] Version {version}: {error}")
```

---

### Example 4: Manual Version Switching

```python
loader.add_shadow_versions("json", ["system"])

# Switch between versions
loader.switch_version("json", "system")

# Execute with current version
def process_data():
    import json
    return json.dumps({"status": "success"})

success, result, error = loader.execute_with_fallback(process_data)
```

---

### Example 5: Logging to File

```python
# Enable file logging
loader = ShadowLoader(verbose=True, log_file="shadow_load.log")

loader.add_shadow_versions("requests", ["2.31.0", "2.28.2"])

def test_connection():
    import requests
    return requests.get("https://example.com")

loader.execute_with_fallback(test_connection, package="requests")

# Check log file
# tail shadow_load.log
# [2026-01-27 18:00:00] [i] [INFO] ShadowLoader initialized
# [2026-01-27 18:00:00] [i] [INFO] Adding shadow versions for requests...
# ...
```

---

## Logging Indicators

| Indicator | Meaning | Example |
|-----------|---------|---------|
| `[i]` | Information/Status | `[i] [INFO] ShadowLoader initialized` |
| `[OK]` | Success | `[OK] [SUCCESS] Loaded requests==2.31.0` |
| `[ERR]` | Error | `[ERR] [ERROR] Failed to load version` |
| `[*]` | Switch/Change | `[*] [SWITCH] Switched to version 2.28.2` |
| `[!]` | Warning | `[!] [WARNING] Version issue detected` |

---

## Real-World Use Cases

### 1. Gradual Library Upgrade

```python
# Test if code works with new version before upgrading
loader = ShadowLoader()
loader.add_shadow_versions("fastapi", ["0.100.0", "0.95.0", "0.90.0"])

def run_api_tests():
    from fastapi import FastAPI
    app = FastAPI()
    # Your tests here
    return True

success, _, _ = loader.execute_with_fallback(
    run_api_tests,
    package="fastapi"
)

if success:
    print(f"Safe to upgrade to {loader.get_active_version('fastapi')}")
```

### 2. Beta → Stable Fallback

```python
# Try beta version, fall back to stable
loader = ShadowLoader()
loader.add_shadow_versions("tensorflow", [
    "2.15.0-beta",  # Try beta first
    "2.14.0"        # Fall back to stable
])

def train_model():
    import tensorflow as tf
    return tf.random.normal((100, 100))

success, result, error = loader.execute_with_fallback(
    train_model,
    package="tensorflow"
)
```

### 3. Compatibility Testing

```python
# Find compatible version combination
packages = {
    "numpy": ["2.0.0", "1.26.0", "1.24.0"],
    "pandas": ["2.1.0", "2.0.0", "1.5.0"]
}

loader = ShadowLoader()
for pkg, versions in packages.items():
    loader.add_shadow_versions(pkg, versions)

def analyze_data():
    import numpy as np
    import pandas as pd
    df = pd.DataFrame(np.random.rand(1000, 5))
    return df.describe()

success, result, error = loader.execute_with_fallback(analyze_data)
```

---

## Advanced Features

### Execution History

Track all version attempts:

```python
loader.execute_with_fallback(my_func, package="requests")
loader.execute_with_fallback(my_func, package="requests")

for entry in loader.execution_history:
    print(f"{entry['status']}: {entry.get('package', 'N/A')} - {entry['timestamp']}")
```

---

### Version Status Monitoring

Check detailed status of each version:

```python
status = loader.version_status
# {
#     'requests': {
#         '2.31.0': 'loaded',
#         '2.28.2': 'loaded',
#         '2.25.1': 'failed: ImportError: ...'
#     }
# }
```

---

## Performance Considerations

1. **Version Isolation**: Each version is loaded independently
2. **Memory Usage**: Multiple versions may increase memory usage
3. **Fallback Order**: Versions are tried in the order provided
4. **Caching**: Use `get_active_version()` to check before re-loading

---

## Troubleshooting

### Issue: Version fails to load

```python
# Check version status
status = loader.version_status['package_name']
print(status)  # Shows error details
```

### Issue: Want to see detailed logs

```python
loader = ShadowLoader(verbose=True, log_file="debug.log")
# All operations logged to both console and file
```

### Issue: Need to reset

```python
# Create new instance
loader = ShadowLoader()
```

---

## Integration with SafeLoader

ShadowLoader works alongside SafeLoader:

```python
from safe_loader import SafeLoader, ShadowLoader

# SafeLoader for general safe loading
safe_loader = SafeLoader()
modules = safe_loader.load_modules(['os', 'sys'])

# ShadowLoader for multi-version management
shadow_loader = ShadowLoader()
shadow_loader.add_shadow_versions("requests", ["2.31.0", "2.28.2"])
```

---

## Summary

ShadowLoader provides enterprise-grade multi-version dependency management with:
- Automatic version switching
- Comprehensive logging
- Fallback mechanisms
- Real-time statistics
- Production-ready reliability

Perfect for gradual library upgrades, compatibility testing, and safe version migrations.

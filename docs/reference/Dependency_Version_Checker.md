# SafeLoader - Dependency Version Checker

## Overview

The **Dependency Version Checker** is a feature in SafeLoader that validates installed package versions against requirements and provides intelligent suggestions for version adjustments (upgrades or downgrades) when conflicts are detected.

## Function: `dependency_version_checker()`

### Purpose

Check whether installed packages satisfy version requirements and suggest compatible versions when issues are found.

### Signature

```python
def dependency_version_checker(
    dependencies: Dict[str, str],
    verbose: bool = True,
    recommendations: Optional[Dict[str, List[str]]] = None,
    available_for_adjustment: Optional[Dict[str, List[str]]] = None,
) -> Dict[str, Any]
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `dependencies` | Dict[str, str] | Required | Package name → version requirement (e.g., `{"pip": ">=24.0"}`) |
| `verbose` | bool | True | Print formatted status output |
| `recommendations` | Dict[str, List[str]] | None | Alternative versions to suggest for missing packages |
| `available_for_adjustment` | Dict[str, List[str]] | None | List of available versions for suggesting upgrades/downgrades |

### Return Value

```python
{
    'all_satisfied': bool,  # All requirements met?
    'results': {
        'package_name': {
            'installed_version': str or None,
            'required_version': str,
            'satisfied': bool,
            'status': 'ok' | 'outdated' | 'missing',
            'recommended_version': str or None,
            'adjustment_suggested': str or None,
            'adjustment_reason': str or None,
            'message': str,
        }
    }
}
```

## Version Operators

The function supports standard Python version operators:

```python
">=1.20.0"    # Greater than or equal (default)
"<=2.0.0"     # Less than or equal
"==1.3.0"     # Exact version
">1.0.0"      # Greater than
"<3.0.0"      # Less than
"1.20.0"      # Defaults to >= if no operator
```

## Status Types

| Status | Meaning | Suggestion |
|--------|---------|-----------|
| `ok` | Version satisfies requirement | No action needed |
| `outdated` | Version too old for requirement | Upgrade or downgrade |
| `missing` | Package not installed | Install with recommended version |

## Usage Examples

### Example 1: Basic Version Check

```python
from safe_loader import dependency_version_checker

result = dependency_version_checker({
    "pip": ">=20.0",
    "setuptools": ">=40.0",
}, verbose=True)

print(f"All satisfied: {result['all_satisfied']}")
```

**Output:**
```
[OK      ] pip                24.0       ✓ requires >=20.0
[OK      ] setuptools         80.9.0     ✓ requires >=40.0
All satisfied: True
```

### Example 2: Handle Missing Packages

```python
result = dependency_version_checker(
    {"numpy": ">=1.20.0", "pandas": ">=1.3.0"},
    recommendations={
        "numpy": ["1.22.0", "1.21.0", "1.20.0"],
        "pandas": ["2.0.0", "1.5.0", "1.3.0"],
    },
    verbose=True
)
```

**Output:**
```
[MISSING ] numpy              requires >=1.20.0     → Install 1.22.0
[MISSING ] pandas             requires >=1.3.0      → Install 2.0.0
```

### Example 3: Suggest Version Adjustment

```python
result = dependency_version_checker(
    {"pip": ">=25.0.0"},
    available_for_adjustment={
        "pip": ["23.0", "24.0", "25.0", "26.0"]
    },
    verbose=True
)

# Get adjustment suggestion
for pkg, info in result['results'].items():
    if info.get('adjustment_suggested'):
        print(f"Upgrade {pkg} to {info['adjustment_suggested']}")
        print(f"Reason: {info['adjustment_reason']}")
```

**Output:**
```
[OUTDATED] pip                24.0       → requires >=25.0.0 → Adjust to 25.0

Upgrade pip to 25.0
Reason: Upgrade to 25.0 to satisfy >=25.0.0
```

### Example 4: Batch Dependency Check

```python
dependencies = {
    "requests": ">=2.20.0",
    "numpy": ">=1.15.0",
    "pandas": ">=0.25.0",
}

result = dependency_version_checker(dependencies, verbose=True)

# Show summary
if result['all_satisfied']:
    print("✅ All dependencies OK")
else:
    for pkg, info in result['results'].items():
        if not info['satisfied']:
            print(f"⚠️  {pkg}: {info['message']}")
```

### Example 5: Process Results Programmatically

```python
result = dependency_version_checker(deps, verbose=False)

# Get installation commands
install_commands = []
for pkg, info in result['results'].items():
    if info['status'] == 'missing':
        cmd = f"pip install {pkg}"
        if info.get('adjustment_suggested'):
            cmd += f"=={info['adjustment_suggested']}"
        install_commands.append(cmd)

for cmd in install_commands:
    print(cmd)
```

## Real-World Scenarios

### Scenario 1: Application Startup Validation

```python
from safe_loader import SafeLoader, dependency_version_checker
import sys

def startup():
    """Validate environment before running application"""
    
    required_deps = {
        "pip": ">=20.0",
        "setuptools": ">=45.0",
        "requests": ">=2.20.0",
    }
    
    result = dependency_version_checker(required_deps, verbose=True)
    
    if not result['all_satisfied']:
        print("\n❌ Environment validation failed!")
        sys.exit(1)
    
    print("\n✅ Environment ready!")

if __name__ == '__main__':
    startup()
    # Run application...
```

### Scenario 2: CI/CD Environment Check

```python
def validate_ci_environment():
    """Ensure CI/CD environment has compatible versions"""
    
    required = {
        "pip": ">=20.0",
        "setuptools": ">=45.0",
        "wheel": ">=0.35.0",
    }
    
    available = {
        "pip": ["20.0", "21.0", "22.0", "23.0", "24.0"],
        "setuptools": ["45.0", "50.0", "60.0", "65.0"],
        "wheel": ["0.35.0", "0.36.0", "0.37.0", "0.42.0"],
    }
    
    result = dependency_version_checker(
        required,
        available_for_adjustment=available,
        verbose=True
    )
    
    return result['all_satisfied']
```

### Scenario 3: Handle Version Conflicts

```python
def resolve_version_conflict(package_name):
    """Try to resolve version conflicts with suggested alternatives"""
    
    try:
        # Attempt to use package
        module = __import__(package_name)
        
    except ImportError as e:
        # Get available versions and suggestions
        result = dependency_version_checker(
            {package_name: ">=1.0.0"},
            available_for_adjustment={
                package_name: ["1.0.0", "1.5.0", "2.0.0"]
            }
        )
        
        info = result['results'][package_name]
        if info.get('adjustment_suggested'):
            print(f"Try: pip install {package_name}=={info['adjustment_suggested']}")
```

### Scenario 4: Integration with SafeLoader

```python
from safe_loader import SafeLoader, dependency_version_checker

with SafeLoader(verbose=True) as loader:
    # Load required modules
    modules = loader.load_modules(['os', 'sys', 'json'])
    
    # Check dependencies
    result = dependency_version_checker({
        "requests": ">=2.20.0",
        "numpy": ">=1.15.0",
    })
    
    if result['all_satisfied']:
        print("✅ All checks passed!")
```

## Output Format

### Verbose Output
```
[OK      ] pip                24.0       ✓ requires >=20.0
[OUTDATED] numpy              1.19.0     → requires >=1.20.0  → Adjust to 1.20.0
[MISSING ] pandas             requires >=1.3.0     → Install 2.0.0
```

### Status Indicators
- `[OK      ]` - Version satisfies requirement
- `[OUTDATED]` - Version doesn't meet requirement (too old)
- `[MISSING ]` - Package not installed
- `✓` - Success/satisfaction indicator
- `→` - Action needed (adjust version)

## Best Practices

### 1. Always Check `all_satisfied`
```python
result = dependency_version_checker(deps)
if not result['all_satisfied']:
    handle_dependency_issues()
```

### 2. Provide Available Versions for Better Suggestions
```python
result = dependency_version_checker(
    deps,
    available_for_adjustment=available_versions  # Enables smart suggestions
)
```

### 3. Use Recommendations for Missing Packages
```python
result = dependency_version_checker(
    deps,
    recommendations={
        "numpy": ["1.22.0", "1.21.0"],
        "pandas": ["2.0.0", "1.5.0"],
    }
)
```

### 4. Validate on Startup, Not on Every Import
```python
def main():
    # Validate once at startup
    if not validate_environment():
        sys.exit(1)
    
    # Then run application normally
    run_app()
```

### 5. Process Results Before Taking Action
```python
result = dependency_version_checker(deps, verbose=False)

for pkg, info in result['results'].items():
    if info['status'] == 'outdated':
        if info.get('adjustment_suggested'):
            log_upgrade_suggestion(pkg, info['adjustment_suggested'])
```

## Integration with SafeLoader

The function integrates seamlessly with SafeLoader's other features:

```python
from safe_loader import SafeLoader, dependency_version_checker, quick_load

# Method 1: Direct use
result = dependency_version_checker(deps)

# Method 2: With SafeLoader context
with SafeLoader() as loader:
    modules = loader.load_modules(['os', 'sys'])
    result = dependency_version_checker(deps)

# Method 3: Combined with quick_load
modules = quick_load('os', 'sys', 'json')
result = dependency_version_checker(deps)
```

## Error Handling

The function handles errors gracefully:

```python
try:
    result = dependency_version_checker(deps)
except Exception as e:
    print(f"Error checking dependencies: {e}")
    # Application continues running
```

## Performance Characteristics

- **Version checking**: O(1) per package using `importlib.metadata`
- **Version comparison**: O(1) per package comparison
- **Sorting versions**: O(m log m) where m = available versions
- **Overall**: O(n + m log m) where n = number of packages

## Troubleshooting

### Built-in Modules Not Found
Built-in modules (os, sys, json) don't have package metadata. Use real packages:
```python
# ❌ Won't work for built-in modules
result = dependency_version_checker({"os": ">=1.0"})

# ✅ Use actual packages
result = dependency_version_checker({"pip": ">=20.0"})
```

### No Suggestions Generated
Ensure you provide available versions:
```python
result = dependency_version_checker(
    {"numpy": ">=1.20.0"},
    available_for_adjustment={"numpy": ["1.19.0", "1.20.0", "1.21.0"]}
)
```

### Version Parsing Issues
The function automatically falls back to string-based comparison if `packaging` library is unavailable.

## API Quick Reference

```python
# Basic check
result = dependency_version_checker({"pip": ">=20.0"})

# With recommendations
dependency_version_checker(
    {"numpy": ">=1.20.0"},
    recommendations={"numpy": ["1.22.0", "1.21.0"]}
)

# With adjustment suggestions
dependency_version_checker(
    {"pip": ">=25.0.0"},
    available_for_adjustment={"pip": ["23.0", "24.0", "25.0"]}
)

# Silent mode
result = dependency_version_checker(deps, verbose=False)

# Verbose mode (default)
result = dependency_version_checker(deps, verbose=True)
```

## See Also

- Main module: `safe_loader.py`
- Examples: `test.py` (Example 10)
- SafeLoader documentation in code docstrings

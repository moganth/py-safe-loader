# 🛡️ py-safe-loader

A robust Python library for safe module loading and code execution that **never crashes your program**. Handle import errors, function failures, and code execution gracefully without terminating your application.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 🌟 Features

### Core Capabilities

- **🔒 Safe Module Loading**: Import modules without crashes - handles missing dependencies gracefully
- **⚡ Safe Function Execution**: Execute any function with automatic error catching
- **📝 Safe Code Execution**: Run code strings and files safely with exec()
- **📊 Detailed Logging**: Built-in logging with timestamps and severity levels
- **📈 Execution Tracking**: Monitor all operations with execution history
- **🎯 Context Manager Support**: Use with Python's `with` statement for automatic cleanup
- **💾 File Logging**: Optionally log all errors to a file
- **🔍 Import Suggestions**: Get helpful installation suggestions for missing packages
- **📋 Summary Reports**: Comprehensive summaries of all operations

## 📦 Installation

### From pip
you can install directly from pip using
```bash
pip install py-safe-loader
```

### From Source
```bash
cd py_safe_loader
pip install -e .
```

### Direct Import
You can also directly copy `safe_loader.py` to your project directory.

## 🚀 Quick Start

### Basic Module Loading

```python
from py_safe_loader import SafeLoader

# Create loader instance
loader = SafeLoader(verbose=True)

# Load modules - missing modules won't crash your program!
modules = loader.load_modules([
    'os',
    'sys',
    'requests',         # Works if installed
    'fake_module',      # Fails gracefully - program continues
    'pandas'
])

# Use loaded modules
if 'os' in modules:
    print(modules['os'].getcwd())
```

### One-Liner Quick Load

```python
from safe_loader import quick_load

# Load modules with a single function call
modules = quick_load('os', 'sys', 'json', 'non_existent_module')
```

### Safe Function Execution

```python
from safe_loader import SafeLoader

loader = SafeLoader()

def risky_function(a, b):
    return a / b  # Might cause division by zero

# Execute safely - returns (success, result, error)
success, result, error = loader.safe_execute(risky_function, 10, 0)

if success:
    print(f"Result: {result}")
else:
    print(f"Error caught: {error}")
    # Your program continues running!
```

### Quick Safe Run

```python
from safe_loader import safe_run

# Quick one-liner for safe function execution
success, result, error = safe_run(lambda: 5 * 5)
```

## 📖 Advanced Usage

### Context Manager (Recommended)

```python
from safe_loader import SafeLoader

with SafeLoader(verbose=True, log_file='errors.log') as loader:
    # Load modules
    modules = loader.load_modules(['os', 'sys', 'requests'])
    
    # Execute functions safely
    def my_function():
        return "Hello, World!"
    
    success, result, error = loader.safe_execute(my_function)

# Automatic summary report and cleanup at context exit
```

### Safe Code Execution

```python
loader = SafeLoader()

# Execute code string
code = """
def greet(name):
    return f"Hello, {name}!"

result = greet("SafeLoader")
"""

success, namespace, error = loader.safe_exec_code(code)

if success:
    print(namespace['result'])  # Access variables from executed code
```

### Safe File Execution

```python
loader = SafeLoader()

# Execute a Python file safely
success, namespace, error = loader.safe_exec_file('script.py')

if success:
    # Access functions and variables from the executed file
    if 'my_function' in namespace:
        namespace['my_function']()
```

### Import with Install Suggestions

```python
loader = SafeLoader()

# Try to import, get helpful message if not installed
requests = loader.try_import_or_install('requests')
pandas = loader.try_import_or_install('pandas')

if requests:
    print("Requests is available!")
else:
    print("Install suggestion shown in console")
```

### Error Logging to File

```python
# All operations will be logged to file
loader = SafeLoader(verbose=True, log_file='app_errors.log')

loader.load_modules(['os', 'fake_module'])

def failing_function():
    raise ValueError("Test error")

loader.safe_execute(failing_function)

# Check 'app_errors.log' for detailed logs
```

### Summary Reports

```python
loader = SafeLoader()

# Perform various operations
loader.load_modules(['os', 'sys', 'fake_module'])

def test_func():
    return 42

loader.safe_execute(test_func)

# Get summary dictionary
summary = loader.get_summary()
print(summary)

# Or print formatted summary
loader.print_summary()
```

## 🎯 Real-World Example

### Building a Robust Application

```python
from safe_loader import SafeLoader

class MyApplication:
    def __init__(self):
        # Initialize with logging
        self.loader = SafeLoader(verbose=True, log_file='app.log')
        
        # Load all dependencies - app continues even if some fail
        self.modules = self.loader.load_modules([
            'requests',      # For HTTP calls
            'pandas',        # For data processing
            'matplotlib',    # For plotting
            'optional_dep'   # Optional feature - won't crash if missing
        ])
        
    def run(self):
        """Main application logic"""
        # Use available modules only
        if 'requests' in self.modules:
            self._fetch_data()
        
        if 'pandas' in self.modules:
            self._process_data()
        
        if 'matplotlib' in self.modules:
            self._create_plots()
        else:
            print("Plotting unavailable - install matplotlib")
        
        # Print summary of what worked and what didn't
        self.loader.print_summary()
    
    def _fetch_data(self):
        def fetch():
            # Your fetch logic
            return self.modules['requests'].get('https://api.example.com')
        
        success, result, error = self.loader.safe_execute(fetch)
        if not success:
            print(f"Data fetch failed: {error}")
            # Application continues with cached data or alternative
    
    def _process_data(self):
        # Similar pattern for other features
        pass
    
    def _create_plots(self):
        # Similar pattern for plotting
        pass

# Run application - guaranteed not to crash on import/execution errors
if __name__ == '__main__':
    app = MyApplication()
    app.run()
```

### Feature Manager Pattern

```python
class FeatureManager:
    """Manage optional features that may or may not be available"""
    
    def __init__(self):
        self.loader = SafeLoader(verbose=False)
        self.features = {}
    
    def load_feature(self, feature_name, module_name):
        """Load an optional feature"""
        module = self.loader.load_module(module_name)
        if module:
            self.features[feature_name] = module
            return True
        return False
    
    def has_feature(self, feature_name):
        """Check if a feature is available"""
        return feature_name in self.features
    
    def use_feature(self, feature_name, func_name, *args, **kwargs):
        """Use a feature if available"""
        if not self.has_feature(feature_name):
            print(f"Feature '{feature_name}' not available")
            return None
        
        func = getattr(self.features[feature_name], func_name, None)
        if func:
            success, result, error = self.loader.safe_execute(func, *args, **kwargs)
            return result if success else None
        return None

# Usage
fm = FeatureManager()
fm.load_feature('web', 'requests')
fm.load_feature('data', 'pandas')
fm.load_feature('ml', 'sklearn')

# Use features conditionally
if fm.has_feature('web'):
    response = fm.use_feature('web', 'get', 'https://api.example.com')
```

## 🔧 API Reference

### SafeLoader Class

#### Constructor
```python
SafeLoader(verbose=True, log_file=None)
```
- `verbose` (bool): Print detailed messages
- `log_file` (str): Optional file path to log errors

#### Methods

**`load_module(module_name: str) -> Optional[Any]`**
- Load a single module safely
- Returns module object or None

**`load_modules(module_names: List[str]) -> Dict[str, Any]`**
- Load multiple modules
- Returns dictionary of successfully loaded modules

**`safe_execute(func: Callable, *args, **kwargs) -> tuple`**
- Execute function safely
- Returns `(success: bool, result: Any, error: str)`

**`safe_exec_code(code: str, namespace: dict = None) -> tuple`**
- Execute code string safely
- Returns `(success: bool, namespace: dict, error: str)`

**`safe_exec_file(file_path: str, namespace: dict = None) -> tuple`**
- Execute Python file safely
- Returns `(success: bool, namespace: dict, error: str)`

**`try_import_or_install(package_name: str, import_name: str = None) -> Optional[Any]`**
- Try to import package with installation suggestion
- Returns module object or None

**`get_summary() -> Dict`**
- Get statistics and details of all operations
- Returns summary dictionary

**`print_summary()`**
- Print formatted summary report

**`reset()`**
- Clear all tracking data

### Convenience Functions

**`quick_load(*module_names, verbose=True) -> Dict[str, Any]`**
- Quick function to load modules without creating loader instance

**`safe_run(func: Callable, *args, **kwargs) -> tuple`**
- Quick function to safely execute any function
- Returns `(success: bool, result: Any, error: str)`

## 📊 Output Examples

### Successful Module Loading
```
[2026-01-22 10:30:15] [INFO] Loading 4 modules...
[2026-01-22 10:30:15] [SUCCESS] ✓ Successfully loaded module: os
[2026-01-22 10:30:15] [SUCCESS] ✓ Successfully loaded module: sys
[2026-01-22 10:30:15] [ERROR] ✗ Failed to load fake_module: Import error: No module named 'fake_module'
[2026-01-22 10:30:15] [SUCCESS] ✓ Successfully loaded module: json
[2026-01-22 10:30:15] [INFO] Loaded 3/4 modules successfully
```

### Summary Report
```
============================================================
SAFELOADER SUMMARY REPORT
============================================================
Total Modules Attempted: 4
Successfully Loaded: 3
Failed to Load: 1

✓ Loaded Modules:
  - os
  - sys
  - json

✗ Failed Modules:
  - fake_module: Import error: No module named 'fake_module'

Execution History (2 operations):
  ✓ test_function - 10:30:20
  ✗ failing_function - 10:30:21
============================================================
```

## 🎨 Use Cases

- **Development**: Test code without crashes during development
- **Production Apps**: Build resilient applications with graceful degradation
- **Plugin Systems**: Load optional plugins without failing on missing ones
- **Data Pipelines**: Continue processing even if some steps fail
- **Scripts**: Write robust automation scripts
- **Testing**: Test error handling without try-except blocks everywhere
- **Prototyping**: Quickly test code snippets safely

## ⚠️ When to Use

**Perfect for:**
- Loading optional dependencies
- Executing untrusted or experimental code
- Building plugin architectures
- Graceful degradation scenarios
- Development and debugging

**Not recommended for:**
- Performance-critical code (adds overhead)
- When you need strict error handling
- When failures should stop execution

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](py_safe_loader/src/py_safe_loader/LICENSE) file for details.

## 👤 Author

**Moganthkumar**
- Email: Raise PR

## 🙏 Acknowledgments

Built with ❤️ to make Python applications more robust and fault-tolerant.

---

**Made with Python 🐍 | Never crash again! 🛡️**

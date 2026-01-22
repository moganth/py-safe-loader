# 🛡️ py-safe-loader

A robust Python library for safe module loading and code execution that **never crashes your program**. Handle import errors, function failures, and code execution gracefully without terminating your application.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 🌟 What is py-safe-loader?

**py-safe-loader** makes your Python applications bulletproof by safely handling module imports and code execution. Missing dependencies? Broken code? No problem - your program keeps running!

### Core Features

- 🔒 **Safe Module Loading** - Import modules without crashes
- ⚡ **Safe Function Execution** - Execute any function with automatic error catching
- 📝 **Safe Code Execution** - Run code strings and files safely
- 📊 **Detailed Logging** - Track all operations with timestamps
- 🎯 **Context Manager Support** - Clean integration with Python's `with` statement

## 📦 Installation

```bash
pip install py-safe-loader
```

[**More installation options →**](docs/guides/installation.md)

## 🚀 Quick Example

```python
from py_safe_loader import SafeLoader

# Create loader
loader = SafeLoader(verbose=True)

# Load modules - missing ones won't crash!
modules = loader.load_modules(['os', 'sys', 'requests', 'fake_module'])

# Execute functions safely
def risky_function(a, b):
    return a / b

success, result, error = loader.safe_execute(risky_function, 10, 0)
if not success:
    print(f"Caught error: {error}")  # Program continues!
```

**Output:**
```
[2026-01-22 10:30:15] [SUCCESS] ✓ Successfully loaded: os
[2026-01-22 10:30:15] [SUCCESS] ✓ Successfully loaded: sys
[2026-01-22 10:30:15] [SUCCESS] ✓ Successfully loaded: requests
[2026-01-22 10:30:15] [ERROR] ✗ Failed to load fake_module
[2026-01-22 10:30:15] [INFO] Loaded 3/4 modules successfully
```

## 📖 Documentation

### Getting Started
- [Installation Guide](docs/guides/installation.md)
- [Quick Start Tutorial](docs/guides/quick-start.md)
- [Advanced Usage](docs/guides/advanced-usage.md)
- [Use Cases & Best Practices](docs/guides/use-cases.md)

### Function Reference

#### SafeLoader Class
- [SafeLoader](docs/reference/SafeLoader.md) - Main class documentation
- [load_module()](docs/reference/load_module.md) - Load a single module
- [load_modules()](docs/reference/load_modules.md) - Load multiple modules
- [safe_execute()](docs/reference/safe_execute.md) - Execute functions safely
- [safe_exec_code()](docs/reference/safe_exec_code.md) - Execute code strings
- [safe_exec_file()](docs/reference/safe_exec_file.md) - Execute Python files
- [try_import_or_install()](docs/reference/try_import_or_install.md) - Import with suggestions
- [get_summary()](docs/reference/get_summary.md) - Get operation statistics
- [print_summary()](docs/reference/print_summary.md) - Print summary report
- [reset()](docs/reference/reset.md) - Clear tracking data

#### Convenience Functions
- [quick_load()](docs/reference/quick_load.md) - Quick module loading
- [safe_run()](docs/reference/safe_run.md) - Quick safe execution

### Examples
- [Robust Application](docs/examples/robust-application.md)
- [Feature Manager Pattern](docs/examples/feature-manager.md)
- [Plugin System](docs/examples/plugin-system.md)

## 🎯 Common Use Cases

✅ **Loading optional dependencies** - App works with or without certain packages  
✅ **Plugin systems** - Load plugins without crashing  
✅ **Development & debugging** - Test code safely  
✅ **Data pipelines** - Continue processing when steps fail  
✅ **Graceful degradation** - Fallback when features unavailable  

❌ **Not for performance-critical code** - Adds overhead  
❌ **Not for critical dependencies** - Some failures should stop execution  

[**Learn more about when to use →**](docs/guides/use-cases.md)

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📄 License

MIT License - see [LICENSE](py_safe_loader/src/py_safe_loader/LICENSE) file for details.

## 👤 Author

**Moganthkumar**

---

**Made with Python 🐍 | Never crash again! 🛡️**

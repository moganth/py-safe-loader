# Installation Guide

## From pip

You can install directly from pip using:

```bash
pip install py-safe-loader
```

## From Source

```bash
cd py_safe_loader
pip install -e .
```

## Direct Import

You can also directly copy `safe_loader.py` to your project directory and use it without installation.

```python
# Just copy safe_loader.py to your project
from safe_loader import SafeLoader

loader = SafeLoader()
```

## Requirements

- Python 3.8 or higher
- No additional dependencies required

## Verify Installation

```python
from py_safe_loader import SafeLoader

loader = SafeLoader()
print("py-safe-loader installed successfully!")
```

## Upgrading

```bash
pip install --upgrade py-safe-loader
```

## Uninstalling

```bash
pip uninstall py-safe-loader
```

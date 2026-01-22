# try_import_or_install

**Class:** `SafeLoader`

Try to import a package and provide installation suggestions if not found.

## Signature

```python
def try_import_or_install(package_name: str, import_name: str = None) -> Optional[Any]
```

## Parameters

- **package_name** (str): Name of the package to install (used in pip install command)
- **import_name** (str, optional): Name used for import (if different from package_name). Default: `None` (uses package_name)

## Returns

- Module object if import successful
- `None` if import fails (with helpful installation message printed)

## Examples

### Basic Usage

```python
from py_safe_loader import SafeLoader

loader = SafeLoader()

# Try to import requests
requests = loader.try_import_or_install('requests')

if requests:
    response = requests.get('https://example.com')
    print(response.status_code)
else:
    print("Requests not available - install suggestion shown")
```

### Different Package and Import Names

Some packages have different names for installation and import:

```python
# Package: 'Pillow', Import: 'PIL'
pil = loader.try_import_or_install('Pillow', import_name='PIL')

# Package: 'python-dateutil', Import: 'dateutil'  
dateutil = loader.try_import_or_install('python-dateutil', import_name='dateutil')

# Package: 'beautifulsoup4', Import: 'bs4'
bs4 = loader.try_import_or_install('beautifulsoup4', import_name='bs4')
```

### Building Optional Features

```python
class MyApp:
    def __init__(self):
        self.loader = SafeLoader(verbose=True)
        
        # Try to load optional dependencies
        self.requests = self.loader.try_import_or_install('requests')
        self.pandas = self.loader.try_import_or_install('pandas')
        self.matplotlib = self.loader.try_import_or_install('matplotlib')
    
    def fetch_data(self):
        if self.requests:
            return self.requests.get('https://api.example.com').json()
        else:
            print("Feature unavailable - install requests")
            return None
    
    def analyze_data(self, data):
        if self.pandas:
            return self.pandas.DataFrame(data)
        else:
            print("Feature unavailable - install pandas")
            return None
```

## Output Example

When package is not installed:

```
[2026-01-22 10:30:15] [ERROR] ✗ Failed to import 'requests'
[2026-01-22 10:30:15] [INFO] To install, run: pip install requests
```

## Notes

- Provides helpful pip install commands for missing packages
- Does NOT automatically install packages (security reasons)
- Handles the common case where package name ≠ import name
- Returns `None` if package not found, allowing graceful degradation

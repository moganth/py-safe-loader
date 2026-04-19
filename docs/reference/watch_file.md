# watch_file

**Class:** `SafeLoader`

Watch a file for changes and automatically hot-reload it safely. If a reload fails, the previous version is kept.

## Signature

```python
def watch_file(file_path: str, file_type: str)
```

## Parameters

- **file_path** (str): Path to the file to watch
- **file_type** (str): Type of file — `'json'` or `'python'`

## Raises

- **ValueError**: If the file does not exist or `file_type` is not `'json'` or `'python'`

## Related Methods

### get_watched_data

```python
def get_watched_data(file_path: str) -> Any
```

Returns the latest loaded data for a watched file.
- For JSON files: returns a `dict`
- For Python files: returns the execution namespace `dict`

Raises `ValueError` if the file is not being watched.

### stop_watching

```python
def stop_watching()
```

Stops all file watchers and cleans up observer threads. Also called automatically when using SafeLoader as a context manager.

## How It Works

1. File is loaded once on `watch_file()` call
2. A background `watchdog` observer monitors the file's directory
3. When the file is modified, it is safely reloaded
4. If reload fails (bad JSON, Python syntax error, etc.), the old data is kept
5. All reload events are logged

## Requirements

```bash
pip install watchdog
```

## Examples

### Watch a JSON Config File

```python
from safe_loader import SafeLoader
import time

with SafeLoader(verbose=True) as loader:
    loader.watch_file("config.json", "json")

    while True:
        config = loader.get_watched_data("config.json")
        print(config)
        time.sleep(1)
```

Edit `config.json` in another terminal — changes appear automatically.

### Watch a Python File

```python
with SafeLoader(verbose=True) as loader:
    loader.watch_file("rules.py", "python")

    data = loader.get_watched_data("rules.py")
    if 'process' in data:
        data['process']()
```

### Manual Stop

```python
loader = SafeLoader()
loader.watch_file("config.json", "json")

# ... later
loader.stop_watching()
```

## Supported File Types

| Type     | Reload Method     | Data Returned          |
|----------|-------------------|------------------------|
| `json`   | `json.load()`     | Parsed dict            |
| `python` | `safe_exec_file()`| Execution namespace    |

## Notes

- Uses `watchdog` library for cross-platform file monitoring
- Watchers run in background daemon threads
- Context manager (`with` block) automatically stops watchers on exit
- Failed reloads never crash the program — old data is preserved
- Multiple files can be watched simultaneously

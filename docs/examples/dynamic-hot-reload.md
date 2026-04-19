# Dynamic Hot Reload Example

Automatically reload configuration or code files when they change on disk — without restarting your application.

## JSON Config Hot Reload

### config.json

```json
{
    "message": "Hello world",
    "value": 1
}
```

### app.py

```python
from safe_loader import SafeLoader
import time

with SafeLoader(verbose=True) as loader:
    loader.watch_file("config.json", "json")

    last = None
    while True:
        config = loader.get_watched_data("config.json")
        if config != last:
            print("Config updated:", config)
            last = config
        time.sleep(1)
```

Run `app.py`, then edit `config.json` in another editor — changes are picked up automatically.

## Python File Hot Reload

### rules.py

```python
def get_discount():
    return 0.10
```

### app.py

```python
from safe_loader import SafeLoader
import time

with SafeLoader(verbose=True) as loader:
    loader.watch_file("rules.py", "python")

    while True:
        ns = loader.get_watched_data("rules.py")
        if 'get_discount' in ns:
            print(f"Current discount: {ns['get_discount']()}")
        time.sleep(2)
```

Change the return value in `rules.py` — the app picks it up on the next loop.

## Error Resilience

If a watched file has errors during reload (bad JSON, Python syntax error), the old version is kept:

```
[2026-02-01 10:00:01] [INFO] 🔄 Hot reloading: config.json
[2026-02-01 10:00:01] [ERROR] ✗ JSON reload failed, keeping old version: ...
```

Your app continues running with the last good data.

## Use Cases

- **Feature flags** — toggle features by editing a JSON file
- **Business rules** — update pricing/discount logic without restart
- **Development** — iterate on code without restarting the server
- **Configuration** — change settings on the fly

## Notes

- Requires `pip install watchdog`
- Watchers are automatically stopped when using `with` block
- Call `loader.stop_watching()` for manual cleanup

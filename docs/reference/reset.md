# reset

**Class:** `SafeLoader`

Clear all tracking data and execution history.

## Signature

```python
def reset()
```

## Parameters

None

## Returns

None

## Example

```python
from py_safe_loader import SafeLoader

loader = SafeLoader()

# Perform some operations
loader.load_modules(['os', 'sys'])
loader.safe_execute(lambda: 42)

# Check current state
summary = loader.get_summary()
print(summary['total_attempted'])  # Output: 2

# Reset all tracking data
loader.reset()

# Verify reset
summary = loader.get_summary()
print(summary['total_attempted'])  # Output: 0
print(summary['loaded_modules'])   # Output: []
print(summary['execution_history'])  # Output: []
```

## Use Cases

### Between Test Runs

```python
loader = SafeLoader()

# Test 1
loader.load_modules(['os', 'sys'])
print(loader.get_summary())

# Clear for Test 2
loader.reset()

# Test 2
loader.load_modules(['json', 'math'])
print(loader.get_summary())  # Only shows Test 2 results
```

### Periodic Cleanup

```python
class LongRunningApp:
    def __init__(self):
        self.loader = SafeLoader()
    
    def process_batch(self, batch_id):
        # Process batch
        self.loader.load_modules(['pandas', 'numpy'])
        
        # Print batch summary
        print(f"Batch {batch_id}:")
        self.loader.print_summary()
        
        # Reset for next batch
        self.loader.reset()
```

## Notes

- Clears all module loading history
- Clears all execution history
- Does NOT unload modules - they remain imported
- Useful for fresh starts without creating a new SafeLoader instance
- Tracking counters reset to 0

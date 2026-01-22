# Building a Robust Application

This example demonstrates how to build an application that gracefully handles missing dependencies.

## Code

```python
from py_safe_loader import SafeLoader

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

## Key Features

- **Graceful Degradation**: App runs with available features
- **Error Logging**: All errors logged to file
- **Summary Reports**: Know what worked and what didn't
- **No Crashes**: Missing dependencies don't terminate the program

## Benefits

1. App works even with missing optional dependencies
2. Clear feedback on what features are available
3. Easy to debug with comprehensive logging
4. User-friendly error messages

# Feature Manager Pattern

Manage optional features that may or may not be available in your application.

## Code

```python
from py_safe_loader import SafeLoader

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

if fm.has_feature('data'):
    df = fm.use_feature('data', 'DataFrame', {'a': [1, 2, 3]})

if fm.has_feature('ml'):
    # Use ML features
    pass
else:
    print("ML features not available - install sklearn")
```

## Use Cases

- **Plugin Systems**: Load optional plugins without crashing
- **Feature Flags**: Enable features based on availability
- **Modular Applications**: Build apps with optional components
- **Development**: Test with subset of dependencies

## Advantages

1. Clean separation of feature management
2. Easy to check feature availability
3. Graceful handling of missing features
4. Reusable pattern across projects

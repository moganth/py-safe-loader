# Plugin System Example

Build a plugin system that loads available plugins without crashing on missing ones.

## Code

```python
from py_safe_loader import SafeLoader
from pathlib import Path

class PluginManager:
    """Load and manage plugins safely"""
    
    def __init__(self, plugin_dir='plugins'):
        self.loader = SafeLoader(verbose=True, log_file='plugins.log')
        self.plugin_dir = Path(plugin_dir)
        self.plugins = {}
    
    def discover_plugins(self):
        """Discover all Python files in plugin directory"""
        if not self.plugin_dir.exists():
            print(f"Plugin directory {self.plugin_dir} not found")
            return []
        
        return list(self.plugin_dir.glob('*.py'))
    
    def load_plugin(self, plugin_file):
        """Load a single plugin file"""
        success, namespace, error = self.loader.safe_exec_file(str(plugin_file))
        
        if success:
            # Look for plugin class or initialization function
            if 'Plugin' in namespace:
                plugin_name = plugin_file.stem
                self.plugins[plugin_name] = namespace['Plugin']()
                print(f"✓ Loaded plugin: {plugin_name}")
                return True
        else:
            print(f"✗ Failed to load {plugin_file.name}: {error}")
        
        return False
    
    def load_all_plugins(self):
        """Load all discovered plugins"""
        plugin_files = self.discover_plugins()
        
        for plugin_file in plugin_files:
            self.load_plugin(plugin_file)
        
        print(f"\nLoaded {len(self.plugins)} plugins")
        return self.plugins
    
    def execute_plugin(self, plugin_name, method_name, *args, **kwargs):
        """Execute a plugin method safely"""
        if plugin_name not in self.plugins:
            print(f"Plugin '{plugin_name}' not loaded")
            return None
        
        plugin = self.plugins[plugin_name]
        if not hasattr(plugin, method_name):
            print(f"Plugin '{plugin_name}' has no method '{method_name}'")
            return None
        
        method = getattr(plugin, method_name)
        success, result, error = self.loader.safe_execute(method, *args, **kwargs)
        
        if success:
            return result
        else:
            print(f"Plugin execution failed: {error}")
            return None

# Usage
if __name__ == '__main__':
    # Create plugin manager
    pm = PluginManager('plugins')
    
    # Load all plugins
    plugins = pm.load_all_plugins()
    
    # Execute plugin methods
    pm.execute_plugin('my_plugin', 'process', data={'key': 'value'})
    pm.execute_plugin('analytics_plugin', 'analyze', dataset=[1, 2, 3])
```

## Example Plugin Structure

```python
# plugins/my_plugin.py

class Plugin:
    """Example plugin"""
    
    def __init__(self):
        self.name = "MyPlugin"
        self.version = "1.0"
    
    def process(self, data):
        """Process some data"""
        return f"Processed: {data}"
    
    def cleanup(self):
        """Cleanup resources"""
        pass
```

## Benefits

1. **Safe Loading**: Broken plugins don't crash the application
2. **Dynamic Discovery**: Automatically find plugins in directory
3. **Error Isolation**: Plugin errors don't affect other plugins
4. **Easy Debugging**: Detailed logs of what failed and why

## Use Cases

- Web application plugins
- Data processing pipelines
- Game modding systems
- IDE extensions

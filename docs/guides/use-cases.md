# Use Cases

## When to Use py-safe-loader

### ✅ Perfect For

#### 1. **Loading Optional Dependencies**
Build applications that work with or without certain packages.

```python
loader = SafeLoader()
modules = loader.load_modules(['pandas', 'matplotlib', 'seaborn'])

# Use only available features
if 'pandas' in modules:
    # Do data processing
    pass

if 'matplotlib' in modules:
    # Create plots
    pass
```

#### 2. **Plugin Systems**
Load plugins without crashing if some are broken or missing dependencies.

```python
# Load all plugins safely
for plugin_file in plugin_directory:
    success, namespace, error = loader.safe_exec_file(plugin_file)
    if success:
        plugins.append(namespace['Plugin']())
```

#### 3. **Development and Debugging**
Test code without crashes during development.

```python
# Test experimental code safely
success, result, error = loader.safe_execute(experimental_function)
if not success:
    print(f"Still has bugs: {error}")
```

#### 4. **Data Pipelines**
Continue processing even if some steps fail.

```python
for step in pipeline_steps:
    success, result, error = loader.safe_execute(step, data)
    if success:
        data = result
    else:
        logger.warning(f"Step failed: {error}, using previous data")
```

#### 5. **Graceful Degradation**
Build robust applications with fallback features.

```python
# Try advanced feature first, fallback to basic
advanced_lib = loader.load_module('advanced_processor')
if advanced_lib:
    result = advanced_lib.process(data)
else:
    result = basic_process(data)
```

#### 6. **Script Automation**
Write robust automation scripts that handle errors gracefully.

```python
# Process files, skip problematic ones
for file in files:
    success, result, error = loader.safe_exec_file(file)
    if not success:
        failed_files.append((file, error))
```

#### 7. **Testing and Prototyping**
Quickly test code snippets without extensive error handling.

```python
# Test multiple approaches
for approach in approaches:
    success, result, error = safe_run(approach, data)
    if success:
        results.append(result)
```

## ⚠️ When NOT to Use

### ❌ Not Recommended For

#### 1. **Performance-Critical Code**
The safety features add overhead. For tight loops or high-performance code, use direct imports.

```python
# DON'T: In performance-critical sections
for i in range(1000000):
    success, result, error = loader.safe_execute(fast_function)

# DO: Use direct imports
import fast_module
for i in range(1000000):
    result = fast_module.fast_function()
```

#### 2. **Strict Error Handling Requirements**
When failures should stop execution, use normal exception handling.

```python
# DON'T: When errors should stop the program
critical_db = loader.load_module('database')
# Program continues even if database module fails!

# DO: Use normal imports for critical dependencies
import database  # Fails fast if missing
```

#### 3. **Production Critical Paths**
For critical production code, explicit error handling is clearer.

```python
# DON'T: Hiding important errors
success, result, error = loader.safe_execute(payment_processor)

# DO: Explicit error handling for critical operations
try:
    result = payment_processor.process()
except PaymentError as e:
    alert_team(e)
    rollback_transaction()
```

## Best Practices

### ✅ DO

- Use for optional features and dependencies
- Combine with explicit checks for critical features
- Use logging to track failures
- Generate summary reports for debugging
- Use context managers for automatic cleanup

### ❌ DON'T

- Use for all imports (only optional ones)
- Ignore errors completely (always check results)
- Use in performance-critical loops
- Hide critical errors that should stop execution
- Skip validation of important results

## Summary

**Use py-safe-loader for:**
- Optional dependencies
- Plugin architectures
- Development and testing
- Graceful degradation
- Robust automation scripts

**Avoid py-safe-loader for:**
- Performance-critical code
- Critical dependencies
- When failures should stop execution
- Production critical paths (without proper validation)

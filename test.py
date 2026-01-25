"""
SafeLoader Usage Examples
=========================
Demonstrates all the ways you can use SafeLoader in your projects
"""

from sys import modules
from safe_loader import SafeLoader, quick_load, safe_run

print("="*60)
print("SAFELOADER - USAGE EXAMPLES")
print("="*60)

# ============================================================================
# EXAMPLE 1: Basic Module Loading
# ============================================================================
print("\n1. BASIC MODULE LOADING")
print("-"*60)

with SafeLoader(verbose=True) as loader:
    modules = loader.load_modules([
        'os',
        'sys', 
        'math',
        'json',
        'non_existent_module',  # This will fail but won't crash
        'datetime'
    ])

# Use the loaded modules
if 'math' in modules:
    print(f"Pi value: {modules['math'].pi}")

if 'datetime' in modules:
    now = modules['datetime'].datetime.now()
    print(f"Current time: {now}")


# ============================================================================
# EXAMPLE 2: Quick Load (Shorthand)
# ============================================================================
print("\n\n2. QUICK LOAD (ONE-LINER)")
print("-"*60)

# Load modules with one line - no need to create loader instance
my_modules = quick_load('os', 'sys', 'json', 'fake_module')

if 'os' in my_modules:
    print(f"Current directory: {my_modules['os'].getcwd()}")


# ============================================================================
# EXAMPLE 3: Safe Function Execution
# ============================================================================
print("\n\n3. SAFE FUNCTION EXECUTION")
print("-"*60)

def risky_division(a, b):
    """This might cause division by zero"""
    return a / b

def buggy_function():
    """This will definitely crash"""
    return undefined_variable + 10

# Execute risky functions safely
success1, result1, error1 = loader.safe_execute(risky_division, 10, 2)
if success1:
    print(f"Division result: {result1}")

success2, result2, error2 = loader.safe_execute(risky_division, 10, 0)
if not success2:
    print(f"Division failed (expected): {error2}")

success3, result3, error3 = loader.safe_execute(buggy_function)
if not success3:
    print(f"Buggy function failed (expected): {error3}")

# Quick safe run
print("\nUsing quick safe_run:")
success, result, error = safe_run(lambda: 5 * 5)
print(f"Lambda result: {result}")


# ============================================================================
# EXAMPLE 4: Safe Code Execution (exec)
# ============================================================================
print("\n\n4. SAFE CODE EXECUTION")
print("-"*60)

# Execute code string safely
code1 = """
def greet(name):
    return f"Hello, {name}!"

result = greet("SafeLoader")
"""

success, namespace, error = loader.sandboxed_exec("Code Execution Test", code1)
if success:
    print(f"Executed code result: {namespace.get('result')}")

# Execute code with syntax error
code2 = """
def broken_function(
    print("This has syntax error")
"""

success, namespace, error = loader.sandboxed_exec("Syntax Error Test", code2)
# Program continues despite syntax error!


# ============================================================================
# EXAMPLE 5: Safe File Execution
# ============================================================================
print("\n\n5. SAFE FILE EXECUTION")
print("-"*60)

# Try to execute a Python file (even if it has errors)
success, namespace, error = loader.safe_exec_file('module1.py')
if success:
    print("File executed successfully!")
    # Access functions from the executed file
    if 'greet' in namespace:
        namespace['greet']()

# Try to execute non-existent file
success, namespace, error = loader.safe_exec_file('non_existent.py')
# Program continues!


# ============================================================================
# EXAMPLE 6: Try Import or Install Suggestion
# ============================================================================
print("\n\n6. TRY IMPORT WITH INSTALL SUGGESTION")
print("-"*60)

# Try to import packages, get helpful message if not installed
requests = loader.try_import_or_install('requests')
numpy = loader.try_import_or_install('numpy')
pandas = loader.try_import_or_install('pandas')

if requests:
    print("Requests is available!")
else:
    print("Requests is not available (see suggestion above)")


# ============================================================================
# EXAMPLE 7: Using in Your Main Application
# ============================================================================
print("\n\n7. REAL-WORLD MAIN.PY EXAMPLE")
print("-"*60)

# This is how you'd use it in your actual main.py

class MyApplication:
    def __init__(self):
        # Initialize SafeLoader
        with SafeLoader(verbose=True, log_file='app_errors.log') as loader:
            self.loader = loader
        
        # Load all your project modules
        self.modules = self.loader.load_modules([
            'module1',
            'module2', 
            'module3_broken',  # Even if this fails, app continues
            'module4'
        ])
        
    def run(self):
        """Main application logic"""
        print("\nApplication is running with available modules...")
        
        # Use loaded modules safely
        if 'module1' in self.modules:
            success, result, error = self.loader.safe_execute(
                self.modules['module1'].greet
            )
        
        if 'module2' in self.modules:
            success, result, error = self.loader.safe_execute(
                self.modules['module2'].module2_function
            )
        
        # Even if some modules failed, the app keeps running!
        print("Application completed successfully!")
        
        # Print summary at the end
        self.loader.print_summary()

# Run the application
app = MyApplication()
app.run()


# ============================================================================
# EXAMPLE 8: Advanced - Conditional Feature Loading
# ============================================================================
print("\n\n8. CONDITIONAL FEATURE LOADING")
print("-"*60)

class FeatureManager:
    def __init__(self):
        with SafeLoader(verbose=False) as loader:
            self.loader = loader
        self.features = {}
        
    def load_feature(self, feature_name, module_name):
        """Load optional features"""
        module = self.loader.load_module(module_name)
        if module:
            self.features[feature_name] = module
            return True
        return False
    
    def has_feature(self, feature_name):
        """Check if feature is available"""
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

# Use feature manager
fm = FeatureManager()
fm.load_feature('web', 'requests')  # Optional web feature
fm.load_feature('data', 'pandas')   # Optional data feature
fm.load_feature('math', 'numpy')    # Optional math feature

if fm.has_feature('math'):
    print("Math features are available!")


# ============================================================================
# EXAMPLE 9: Error Logging to File
# ============================================================================
print("\n\n9. ERROR LOGGING TO FILE")
print("-"*60)

# Create loader with file logging
with SafeLoader(verbose=True, log_file='my_app_errors.log') as logged_loader:

# All errors will be logged to file
    logged_loader.load_modules(['os', 'fake_module', 'sys'])

    def failing_function():
        raise ValueError("This is a test error")

    logged_loader.safe_execute(failing_function)

print("Check 'my_app_errors.log' for detailed error logs!")

# ============================================================================
# EXAMPLE 10: Sandboxed Code Execution
# ============================================================================
print("\n\n10. SANDBOXED CODE EXECUTION (SECURITY TEST)")
print("-" * 60)

# Initialize SafeLoader for sandbox testing
with SafeLoader(verbose=False) as sandbox_loader:

    # --- TEST 1: Legitimate Logic (Should Pass) ---
    valid_code = """
x = 10
y = 20
result = sum([x, y, 30])
print(f'Sandbox Calculation: {result}')
"""
    success, res, err = sandbox_loader.sandboxed_exec("Math & Logic Check", valid_code)
    if success:
        print(f"Test 1 PASSED. Result in Namespace: {res.get('result')}")

    # --- TEST 2: Attempting to Import (Should be Blocked) ---
    malicious_code = """
import os
print(os.getcwd())
"""
    success, res, err = sandbox_loader.sandboxed_exec("Restricted Import Check", malicious_code)
    # The output of this call will automatically show the "RESULT: ❌ BLOCKED" format

    # --- TEST 3: Attempting to Open File (Should be Blocked) ---
    io_code = """
with open('secrets.txt', 'w') as f:
    f.write('pwned')
"""
    # Test with allow_io=False (default)
    success, res, err = sandbox_loader.sandboxed_exec("File System Protection", io_code, allow_io=False)

    # Final Summary for Example 10
    print("\n--- Final Security Audit Table ---")
    sandbox_loader.print_summary()

print("Example 10 Completed. Notice how the program didn't crash during malicious attempts!")
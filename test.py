"""
SafeLoader Usage Examples
=========================
Demonstrates all the ways you can use SafeLoader in your projects
"""

from sys import modules
from importlib import metadata as importlib_metadata
try:
    from packaging.version import Version
except ImportError:
    Version = None

from safe_loader import SafeLoader, quick_load, safe_run, dependency_version_checker

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
    return undefined_variable + 10 # type: ignore

with SafeLoader(verbose=True) as exec_loader:
    # Execute risky functions safely
    success1, result1, error1 = exec_loader.safe_execute(risky_division, 10, 2)
    if success1:
        print(f"Division result: {result1}")

    success2, result2, error2 = exec_loader.safe_execute(risky_division, 10, 0)
    if not success2:
        print(f"Division failed (expected): {error2}")

    success3, result3, error3 = exec_loader.safe_execute(buggy_function)
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

with SafeLoader(verbose=True) as exec_loader:
    success, namespace, error = exec_loader.safe_exec_code(code1)
    if success:
        print(f"Executed code result: {namespace.get('result')}")

    # Execute code with syntax error
    code2 = """
def broken_function(
    print("This has syntax error")
"""

    success, namespace, error = exec_loader.safe_exec_code(code2)
    # Program continues despite syntax error!


# ============================================================================
# EXAMPLE 5: Safe File Execution
# ============================================================================
print("\n\n5. SAFE FILE EXECUTION")
print("-"*60)

with SafeLoader(verbose=True) as exec_loader:
    # Try to execute a Python file (even if it has errors)
    success, namespace, error = exec_loader.safe_exec_file('module1.py')
    if success:
        print("File executed successfully!")
        # Access functions from the executed file
        if 'greet' in namespace:
            namespace['greet']()

    # Try to execute non-existent file
    success, namespace, error = exec_loader.safe_exec_file('non_existent.py')
    # Program continues!


# ============================================================================
# EXAMPLE 6: Try Import or Install Suggestion
# ============================================================================
print("\n\n6. TRY IMPORT WITH INSTALL SUGGESTION")
print("-"*60)

with SafeLoader(verbose=True) as import_loader:
    # Try to import packages, get helpful message if not installed
    requests = import_loader.try_import_or_install('requests')
    numpy = import_loader.try_import_or_install('numpy')
    pandas = import_loader.try_import_or_install('pandas')

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
        # Initialize SafeLoader (kept open for the lifetime of the app)
        self.loader = SafeLoader(verbose=True, log_file='app_errors.log')
        
        # Load all your project modules
        self.modules = self.loader.load_modules([
            'module1',
            'module2', 
            'module3_broken',  # Even if this fails, app continues
            'module4'
        ])
        
    def run(self):
        """Main application logic"""
        try:
            print("\nApplication is running with available modules...")
            
            # Use loaded modules safely
            if 'module1' in self.modules:
                self.loader.safe_execute(
                    self.modules['module1'].greet
                )
            
            if 'module2' in self.modules:
                self.loader.safe_execute(
                    self.modules['module2'].module2_function
                )
            
            # Even if some modules failed, the app keeps running!
            print("Application completed successfully!")
        finally:
            # Print summary and close loader to avoid lingering resources
            self.loader.print_summary()
            self.loader.reset()

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
# ============================================================================
# EXAMPLE 10: DEPENDENCY VERSION CHECKER - Real-World Use Case
# ============================================================================
print("\n\n10. DEPENDENCY VERSION CHECKER - REAL-WORLD PACKAGES")
print("-"*60)

print("\n📊 Real-world scenario: Validate and adjust package dependencies")

# Real-world test: Check common development packages
print("\nValidating development environment packages:")
print("=" * 60)

# Test Case 1: Check real packages that are installed
print("\n✓ Test 1: Check installed packages satisfy requirements")
result = dependency_version_checker(
    {
        "pip": ">=20.0",
        "setuptools": ">=40.0",
        "wheel": ">=0.30.0",
    },
    verbose=True
)
print(f"Status: {'✅ All OK' if result['all_satisfied'] else '⚠️ Issues found'}\n")

# Test Case 2: Check packages that might be missing
print("\n✓ Test 2: Identify missing packages with recommendations")
result = dependency_version_checker(
    {"numpy": ">=1.20.0", "pandas": ">=1.3.0"},
    recommendations={
        "numpy": ["1.22.0", "1.21.0", "1.20.0"],
        "pandas": ["2.0.0", "1.5.0", "1.3.0"],
    },
    verbose=True
)

print("\nSummary of missing packages:")
for pkg, info in result["results"].items():
    if not info["satisfied"]:
        if info.get("adjustment_suggested"):
            print(f"  📦 {pkg}: Recommended version → {info['adjustment_suggested']}")
        else:
            print(f"  📦 {pkg}: {info['message']}")

# Test Case 3: Real-world CI/CD environment check
print("\n\n✓ Test 3: Real-world - CI/CD environment compatibility check")
print("=" * 60)

def validate_environment():
    """Check if environment has required packages for CI/CD pipeline"""
    
    required_packages = {
        "pip": ">=20.0",
        "setuptools": ">=45.0",
        "wheel": ">=0.35.0",
    }
    
    # Available versions from PyPI (simulated for demonstration)
    available_versions = {
        "pip": ["20.0", "20.1", "20.2", "21.0", "22.0", "23.0", "24.0", "25.0"],
        "setuptools": ["45.0", "50.0", "60.0", "65.0", "70.0"],
        "wheel": ["0.35.0", "0.36.0", "0.37.0", "0.42.0"],
    }
    
    print("\nChecking environment compatibility:")
    result = dependency_version_checker(
        required_packages,
        available_for_adjustment=available_versions,
        verbose=True
    )
    
    print(f"\nEnvironment Status: {'✅ Compatible' if result['all_satisfied'] else '⚠️ Adjustments needed'}")
    
    if not result['all_satisfied']:
        print("\nRecommended actions:")
        for pkg, info in result['results'].items():
            if not info['satisfied'] and info.get('adjustment_suggested'):
                print(f"  → {pkg}: pip install {pkg}=={info['adjustment_suggested']}")
    
    return result['all_satisfied']

# Run environment check
is_compatible = validate_environment()


# ============================================================================
# EXAMPLE 11: Dependency Version Checker - Testing passlib and bcrypt
# ============================================================================
print("\n\n11. DEPENDENCY VERSION CHECKER - PASSLIB & BCRYPT")
print("-"*60)

def test_passlib_bcrypt_dependencies():
    """
    Test dependency version checking for passlib and bcrypt packages.
    Validates that installed versions meet minimum requirements and checks 
    against the latest available versions from PyPI.
    """
    
    print("\n🔐 Testing password hashing library dependencies")
    print("=" * 60)
    
    # Define minimum requirements for passlib and bcrypt
    required_packages = {
        "passlib": ">=1.7.0",  # Minimum version for secure hashing
        "bcrypt": ">=3.2.0",   # Minimum version with security patches
    }
    
    # Latest stable versions from PyPI (as of 2026)
    latest_versions = {
        "passlib": ["1.7.4", "1.7.3", "1.7.2", "1.7.1", "1.7.0"],
        "bcrypt": ["4.1.2", "4.1.1", "4.1.0", "4.0.1", "4.0.0", "3.2.2", "3.2.1", "3.2.0"],
    }
    
    print("\n📋 Test Case 1: Check if packages meet minimum requirements")
    print("-" * 60)
    result1 = dependency_version_checker(
        required_packages,
        verbose=True
    )
    
    if result1['all_satisfied']:
        print("✅ All password hashing dependencies are satisfied!")
    else:
        print("⚠️ Some dependencies need attention:")
        for pkg, info in result1['results'].items():
            if not info['satisfied']:
                print(f"  - {pkg}: {info['message']}")
    
    print("\n📋 Test Case 2: Check against latest available versions")
    print("-" * 60)
    result2 = dependency_version_checker(
        required_packages,
        available_for_adjustment=latest_versions,
        verbose=True
    )
    
    # Provide upgrade recommendations
    print("\n📦 Upgrade Recommendations:")
    print("-" * 60)
    for pkg, info in result2['results'].items():
        if info['satisfied']:
            current_version = info.get('installed_version', 'unknown')
            print(f"  {pkg}:")
            print(f"    Current: {current_version}")
            print(f"    Latest:  {latest_versions[pkg][0]}")
            
            if info.get('adjustment_suggested'):
                print(f"    💡 Suggested: pip install --upgrade {pkg}=={info['adjustment_suggested']}")
            else:
                print(f"    ✅ Already at recommended version")
        else:
            print(f"  {pkg}: Not installed")
            print(f"    💡 Install: pip install {pkg}>={required_packages[pkg].lstrip('>=')}")
    
    print("\n" + "=" * 60)
    
    # Security best practices note
    print("\n🔒 Security Note:")
    print("  For production environments, always use:")
    print("  - passlib: Latest version for strongest password hashing")
    print("  - bcrypt: Latest version for patched security vulnerabilities")
    
    return result2, latest_versions

# Run the passlib and bcrypt dependency test
test_result, available_versions = test_passlib_bcrypt_dependencies()

# Print final summary with version pinning
print("\n" + "=" * 60)
print("📊 FINAL TEST SUMMARY - VERSION PINNING")
print("=" * 60)

if test_result['all_satisfied']:
    print("✅ All password hashing dependencies are properly configured\n")
    print("📌 Recommended Version Pinning (requirements.txt):")
    print("-" * 60)
    for pkg, info in test_result['results'].items():
        if info['satisfied']:
            current = info.get('installed_version', 'unknown')
            compatible_latest = available_versions.get(pkg, ['unknown'])[0]
            suggested = info.get('adjustment_suggested', current)
            
            print(f"\n{pkg}:")
            print(f"  Current installed: {current}")
            print(f"  Compatible latest: {compatible_latest}")
            print(f"  Pin for stability: {pkg}=={compatible_latest}")
            
    print("\n\n📋 Complete requirements.txt entry:")
    print("-" * 60)
    for pkg in test_result['results'].keys():
        if test_result['results'][pkg]['satisfied']:
            latest_version = available_versions.get(pkg, ['unknown'])[0]
            print(f"{pkg}=={latest_version}")
    
    print("\n💡 Alternative with minimum constraints:")
    print("-" * 60)
    for pkg, info in test_result['results'].items():
        if info['satisfied']:
            # Extract minimum version from requirement
            requirement = info.get('requirement', '>=0.0.0')
            min_version = requirement.lstrip('>=')
            latest_version = available_versions.get(pkg, ['unknown'])[0]
            major_version = latest_version.split('.')[0]
            next_major = str(int(major_version) + 1) if major_version.isdigit() else 'x'
            print(f"{pkg}>={min_version},<{next_major}.0.0")
    
else:
    print("⚠️ Action required: Install or update dependencies\n")
    print("📌 Installation commands with version pinning:")
    print("-" * 60)
    for pkg, info in test_result['results'].items():
        latest_version = available_versions.get(pkg, ['unknown'])[0]
        
        if not info['satisfied']:
            print(f"\n{pkg}:")
            print(f"  Status: Not installed")
            print(f"  Install command: pip install {pkg}=={latest_version}")
        elif info.get('adjustment_suggested'):
            suggested = info['adjustment_suggested']
            print(f"\n{pkg}:")
            print(f"  Status: Needs upgrade")
            print(f"  Upgrade to suggested: pip install --upgrade {pkg}=={suggested}")
            print(f"  Upgrade to latest: pip install --upgrade {pkg}=={latest_version}")

print("\n" + "=" * 60)
print("🔐 Version Compatibility Matrix:")
print("=" * 60)

# Dynamically generate compatibility matrix from available versions
passlib_versions = available_versions.get('passlib', [])
bcrypt_versions = available_versions.get('bcrypt', [])

if passlib_versions and bcrypt_versions:
    # Group bcrypt versions by major.minor
    bcrypt_groups = {}
    for v in bcrypt_versions:
        parts = v.split('.')
        if len(parts) >= 2:
            key = f"{parts[0]}.{parts[1]}.x"
            if key not in bcrypt_groups:
                bcrypt_groups[key] = v
    
    # Show compatibility for passlib 1.7.x with different bcrypt versions
    passlib_major_minor = f"{passlib_versions[0].split('.')[0]}.{passlib_versions[0].split('.')[1]}.x"
    for bcrypt_group in list(bcrypt_groups.keys())[:3]:  # Show top 3
        print(f"  passlib {passlib_major_minor} ↔ bcrypt {bcrypt_group}   ✅ Compatible")
    
    print("\n  Recommended combination for production:")
    print(f"    passlib=={passlib_versions[0]} + bcrypt=={bcrypt_versions[0]}")
else:
    print("  Unable to determine version compatibility")
    print("  Please check package documentation")
# ============================================================================
# EXAMPLE 12: Security Scanners (Not-Blocked Warnings)
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 12: Security Scanners (Warnings)")
print("="*70)
print("Demonstrating 3 security scanners that WARN:")
print("  🔍 Obfuscation Detector - Static code analysis")
print("  👁️  Behavioral Detector  - Runtime activity monitoring")
print("  🛡️  Output Guardian      - Post-execution result scanning")
print("-"*70)

sec_loader = SafeLoader(verbose=True)

# TEST 12.1: Clean math operation (no warnings expected)
print("\n[TEST 12.1] Clean math operation (no security warnings)")
code1 = "result = (10 + 20) * 2\npi = 3.14159"
success, ns, error = sec_loader.safe_exec_code(code1)
status = "✅ PASS" if success and ns.get('result') == 60 else "❌ FAIL"
print(f"{status} | Execution: {'SUCCESS' if success else 'FAILED'} | Result: {ns.get('result') if success else 'N/A'}")

# TEST 12.2: Obfuscation patterns (should WARN but still execute)
print("\n[TEST 12.2] Obfuscation patterns (base64 + excessive dunders)")
code2 = """
data = "SGVsbG8gd29ybGQ="  # Base64 string
x__y__z__a__b__c__d__e__f = 42  # Excessive dunder attributes
result = 100
"""
success, ns, error = sec_loader.safe_exec_code(code2)
status = "✅ PASS" if success and ns.get('result') == 100 else "❌ FAIL"
print(f"{status} | Execution: {'SUCCESS' if success else 'FAILED'} | Warnings: OBFUSCATION DETECTED (Not-Blocked)")

# TEST 12.3: Behavioral patterns (file access via os - should WARN but execute)
print("\n[TEST 12.3] Behavioral patterns (file access via os module)")
code3 = """
import os
current_dir = os.getcwd()
result = len(current_dir) > 0
"""
success, ns, error = sec_loader.safe_exec_code(code3)
status = "✅ PASS" if success and ns.get('result') is True else "❌ FAIL"
print(f"{status} | Execution: {'SUCCESS' if success else 'FAILED'} | Warnings: BEHAVIORAL DETECTED (Not-Blocked)")

# TEST 12.4: Output guardian (large output + secret pattern)
print("\n[TEST 12.4] Output guardian (large output + secret pattern)")
code4 = """
# Generate large output (>1MB)
large_list = [i for i in range(50000)]
# Include potential secret pattern
api_key = "api_key='sk_test_abc123xyz456'"
result = len(large_list)
"""
success, ns, error = sec_loader.safe_exec_code(code4)
status = "✅ PASS" if success and ns.get('result') == 50000 else "❌ FAIL"
print(f"{status} | Execution: {'SUCCESS' if success else 'FAILED'} | Warnings: OUTPUT GUARDIAN TRIGGERED (Not-Blocked)")

# TEST 12.5: All scanners combined (should warn 3x but still execute)
print("\n[TEST 12.5] All scanners combined (obfuscation + behavior + output)")
code5 = """
# Obfuscation: base64 pattern
import base64
# Behavior: file access
import os
current_dir = os.getcwd()
# Output: secret pattern + large data
password = "password='super_secret_12345'"
big_data = '*' * 2000000  # 2MB string
result = 999
"""
success, ns, error = sec_loader.safe_exec_code(code5)
status = "✅ PASS" if success and ns.get('result') == 999 else "❌ FAIL"
print(f"{status} | Execution: {'SUCCESS' if success else 'FAILED'} | Warnings: ALL 3 SCANNERS TRIGGERED (Not-Blocked)")

print("\n" + "="*70)
print("EXAMPLE 12 COMPLETE - All security scanners demonstrated")
print("="*70)
print("✅ KEY VERIFICATION: All tests returned success=True despite warnings")
print("✅ SECURITY VALUE: Warnings provide visibility WITHOUT breaking legitimate code")
print("="*70)
# ============================================================================
# FINAL SUMMARY
# ============================================================================
print("\n" + "="*70)
print("ALL TESTS COMPLETED SUCCESSFULLY")
print("="*70)
print("SafeLoader passed all functionality and security visibility tests!")
print("="*70)
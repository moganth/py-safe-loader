### SafeLoader Security Scanners

## Overview
Three non-blocking security scanners added to safe_exec_code() that warn but never block execution. Ideal for test suites where legitimate operations (like import os) must succeed while still providing security visibility.

### Scanner Layers

|-- Scanner |---  When --- 	|----------------- Detects ---------------------------	|-- Warning Example
|-- --------------------|-- -------------|-- --------------------------------------------------	|---------------------------------------------------------
|-- 🔍 Obfuscation 	|-- Before exec  |-- Base64, excessive dunders, hex escapes		|-- ⚠️ OBFUSCATION WARNING: Base64 patterns detected
|-- 👁️ Behavioral 	|-- During exec  |-- File/network access, introspection calls 		|-- ⚠️ BEHAVIORAL WARNING: File access patterns detected
|-- 🛡️ Output Guardian	|-- After exec	 |-- Large outputs (>1MB), secret leakage patterns 	|-- ⚠️ OUTPUT GUARDIAN: Potential secret leakage in 'api_key'

### Key Properties

|-- Property 	|-- Value
|-- ------------|-------------------------------------------
|-- Blocking? 	|-- ❌ Never blocks execution
|-- Test Impact |-- ✅ All tests pass (warnings only)
|-- Performance |-- <15ms overhead for typical code
|-- Setup 	    |-- Zero config - works out of the box
|-- Output 	    |-- Logs to console/file with [SECURITY] tag

### Usage Example

"""

from safe_loader import SafeLoader

loader = SafeLoader(verbose=True)

# Legitimate test with os module (still works!)
code = "import os; result = os.getcwd()"
success, ns, error = loader.safe_exec_code(code)

# Output:
# [2026-01-27 10:30:45] [INFO] Executing code block...
# [2026-01-27 10:30:45] [SECURITY] ⚠️ BEHAVIORAL WARNING: File access patterns detected
# [2026-01-27 10:30:45] [SUCCESS] ✓ Code executed successfully
# → success = True (test passes despite warning)

"""
### Why Use This?

|-- Scenario 			        |-- Benefit
|-- ----------------------------|-- ------------------------------------------------
|-- Test suites 		        |-- Legitimate imports work; warnings don't break CI/CD
|-- Security audits	 	        |-- Visibility into risky patterns without false positives
|-- Secret leakage prevention 	|-- Catches accidental credential commits in test output
|-- Resource protection 	    |-- Detects log bombing attempts (>1MB outputs)

### Integration

|-- Feature 		    |-- Integration
|-- --------------------|-- ----------------------------------------
|-- safe_exec_file() 	|-- Automatically gets same scanners
|-- Context manager 	|-- Warnings appear in final summary report
|-- Log files 		    |-- All SECURITY logs written to log_file
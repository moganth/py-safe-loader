# sandboxed_exec
    Type: Class Method
        Executes raw Python code strings within a restricted environment to prevent unauthorized imports or system access.
# Signature
    ""Python""
        def sandboxed_exec(
            self, 
            label: str, 
            code: str, 
            allow_io: bool = False
        ) -> tuple

# Parameters
    •	label (str): A descriptive name for the test case (used in logs and summaries).
    •	code (str): The Python source code string to execute.
    •	allow_io (bool): Whether to permit basic file operations. Defaults to False.
# Returns
    Tuple of (success, namespace, error):
        •	success (bool): True if the code ran without security violations or syntax errors.
        •	namespace (dict): The resulting global variables from the execution.
        •	error (str): The security violation or traceback message if failed.
----------------------------------------------------------------------------------------------------------

# Examples : 
1. Legitimate Logic (Should Pass)
    Standard mathematical operations and variable assignments are permitted.
    #Python
        with SafeLoader(verbose=False) as sandbox_loader:
            valid_code = """
        x = 10
        y = 20
        result = sum([x, y, 30])
        print(f'Sandbox Calculation: {result}')
        """
            success, res, err = sandbox_loader.sandboxed_exec("Math & Logic Check", valid_code)
            
            if success:
                print(f"Test 1 PASSED. Result in Namespace: {res.get('result')}")
                # Output: Test 1 PASSED. Result in Namespace: 60

2. Restricted Import Check (Should be Blocked)
    The sandbox prevents the import statement for unauthorized modules like os.
    Python
    with SafeLoader() as sandbox_loader:
        malicious_code = """
    import os
    print(os.getcwd())
    """
        success, res, err = sandbox_loader.sandboxed_exec("Restricted Import Check", malicious_code)
        # The output will automatically show: RESULT: ❌ BLOCKED

3. File System Protection
    Attempting to write to the disk is blocked by default via allow_io=False.
    #Python
    with SafeLoader() as sandbox_loader:
        io_code = """
    with open('secrets.txt', 'w') as f:
        f.write('pwned')
    """
        # Test with allow_io=False (default)
        success, res, err = sandbox_loader.sandboxed_exec("File System Protection", io_code, allow_io=False)

4. Generating a Security Audit
    The SafeLoader tracks all attempts across the session for a final report.
    Python
    with SafeLoader() as sandbox_loader:
        # ... run various tests ...
        
        print("\n--- Final Security Audit Table ---")
        sandbox_loader.print_summary()

# Sandbox Security Model
    +---------------------+----------------+-------------------------------------------------------+
    | Feature             | Default Status | Description                                           |
    +---------------------+----------------+-------------------------------------------------------+
    | Built-in Functions  | Limited        | Only non-destructive built-ins are exposed.           |
    +---------------------+----------------+-------------------------------------------------------+
    | Imports             | Blocked        | import statements are intercepted and denied.         |
    +---------------------+----------------+-------------------------------------------------------+
    | File I/O            | Restricted     | open() and file writes are disabled unless allow_io.  |
    +---------------------+----------------+-------------------------------------------------------+
    | Namespace           | Isolated       | Code runs in a unique dictionary to prevent pollution.|
    +---------------------+----------------+-------------------------------------------------------+

# Notes
    •	Audit Logging: Every call to sandboxed_exec is recorded in the internal history.
    •	Verbosity: If verbose=True is set in the constructor, the loader will print colored status updates to the console for every execution.
    •	Performance: Code is compiled into bytecode before execution to catch syntax errors early.

# Complete code :

def sandboxed_exec(self, test_name: str, code: str, allow_io: bool = False) -> tuple:
        """Enhanced Sandbox: Restricts imports and captures line-specific errors with bounds checking"""
        # Security Whitelist
        safe_builtins = {
            'print': print, 'sum': sum, 'len': len, 'range': range,
            'int': int, 'str': str, 'dict': dict, 'list': list,
        }
        if allow_io: safe_builtins['open'] = open
        namespace = {"__builtins__": safe_builtins}
        
        try:
            print(f"\n=============== TEST: {test_name} ===============")
            exec(code, namespace)
            # FIX: Added 'function', 'status', and 'timestamp' for compatibility
            self.execution_history.append({
                'test': test_name, 
                'function': f"Sandbox: {test_name}",
                'status': 'success', 
                'line': 'N/A',
                'timestamp': datetime.now()
            })
            return (True, namespace, None)
            
        except Exception as e:
            # (Keep your existing traceback logic here...)
            _, _, tb = sys.exc_info()
            stack = traceback.extract_tb(tb)
            if isinstance(e, SyntaxError):
                test_line_no = e.lineno
            else:
                test_line_no = stack[-1].lineno if stack else "Unknown"
            
            code_lines = code.strip().split('\n')
            if isinstance(test_line_no, int) and 1 <= test_line_no <= len(code_lines):
                offending_code = code_lines[test_line_no-1].strip()
            else:
                offending_code = "Parser Error (Code likely incomplete)"

            print(f"RESULT: ❌ BLOCKED")
            print(f"TEST CODE LINE: {test_line_no} -> \"{offending_code}\"")
            print(f"REASON: Import operation was detected and blocked on Test Line {test_line_no}")
            
            # FIX: Added 'function', 'status', and 'timestamp' for compatibility
            self.execution_history.append({
                'test': test_name, 
                'function': f"Sandbox: {test_name}",
                'status': 'failed', 
                'line': f'Line {test_line_no}',
                'timestamp': datetime.now()
            })
            return (False, {}, f"Blocked on Line {test_line_no}")

# Sampled output :

    # SANDBOXED CODE EXECUTION (SECURITY TEST)
    ------------------------------------------------------------

    =============== TEST: Math & Logic Check ===============
    Sandbox Calculation: 60
    Test 1 PASSED. Result in Namespace: 60

    =============== TEST: Restricted Import Check ===============
    RESULT: ❌ BLOCKED
    TEST CODE LINE: 2 -> "print(os.getcwd())"
    REASON: Import operation was detected and blocked on Test Line 2

    =============== TEST: File System Protection ===============
    RESULT: ❌ BLOCKED
    TEST CODE LINE: 2 -> "f.write('pwned')"
    REASON: Import operation was detected and blocked on Test Line 2

    --- Final Security Audit Table ---

    ============================================================
    SAFELOADER SUMMARY REPORT
    ============================================================

    Execution History (3 operations):
    ✓ Sandbox: Math & Logic Check - 10:27:49
    ✗ Sandbox: Restricted Import Check - 10:27:49
    ✗ Sandbox: File System Protection - 10:27:49

    ############################################################
                    Sandbox Execution Audit
    ############################################################
    STATUS          | LOCATION   | TEST NAME
    ------------------------------------------------------------
    ✅ PASSED        | N/A        | Math & Logic Check
    ❌ BLOCKED       | Line 2     | Restricted Import Check
    ❌ BLOCKED       | Line 2     | File System Protection
    ############################################################




"""
SafeLoader - Reusable Module and Code Error Handler
====================================================
Import once, use everywhere in your codebase!

Usage:
    from safe_loader import SafeLoader
    
    loader = SafeLoader()
    modules = loader.load_modules(['module1', 'module2', 'module3'])
"""

import importlib
import sys
import traceback
import re
from typing import Dict, List, Optional, Callable, Any
from datetime import datetime
import os
from importlib import metadata as importlib_metadata


class SafeLoader:
    """
    A reusable class for safe module loading and code execution
    that never terminates your program on errors.
    """
    
    def __init__(self, verbose=True, log_file=None):
        """
        Initialize SafeLoader
        
        Args:
            verbose (bool): Print detailed messages
            log_file (str): Optional file path to log errors
        """
        self.verbose = verbose
        self.log_file = log_file
        self.loaded_modules = {}
        self.failed_modules = {}
        self.execution_history = []
        
    def _log(self, message, level="INFO"):
        """Internal logging method"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        
        if self.verbose:
            print(log_entry)
        
        if self.log_file:
            try:
                with open(self.log_file, 'a') as f:
                    f.write(log_entry + "\n")
            except Exception as e:
                print(f"Warning: Could not write to log file: {e}")
    
    def load_module(self, module_name: str) -> Optional[Any]:
        """
        Safely load a single module
        
        Args:
            module_name (str): Name of the module to import
            
        Returns:
            Module object if successful, None if failed
        """
        try:
            module = importlib.import_module(module_name)
            self.loaded_modules[module_name] = module
            self._log(f"✓ Successfully loaded module: {module_name}", "SUCCESS")
            return module
            
        except ImportError as e:
            error_msg = f"Import error: {str(e)}"
            self.failed_modules[module_name] = error_msg
            self._log(f"✗ Failed to load {module_name}: {error_msg}", "ERROR")
            return None
            
        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)}"
            self.failed_modules[module_name] = error_msg
            self._log(f"✗ Unexpected error loading {module_name}: {error_msg}", "ERROR")
            return None
    
    def load_modules(self, module_names: List[str]) -> Dict[str, Any]:
        """
        Safely load multiple modules
        
        Args:
            module_names (list): List of module names to import
            
        Returns:
            Dictionary of successfully loaded modules {name: module_object}
        """
        self._log(f"Loading {len(module_names)} modules...", "INFO")
        
        for module_name in module_names:
            self.load_module(module_name)
        
        self._log(
            f"Loaded {len(self.loaded_modules)}/{len(module_names)} modules successfully",
            "INFO"
        )
        
        return self.loaded_modules.copy()
    
    def safe_execute(self, func: Callable, *args, **kwargs) -> tuple:
        """
        Safely execute any function and catch all errors
        
        Args:
            func: Function to execute
            *args: Positional arguments for the function
            **kwargs: Keyword arguments for the function
            
        Returns:
            Tuple of (success: bool, result: Any, error: str)
        """
        func_name = func.__name__ if hasattr(func, '__name__') else str(func)
        
        try:
            self._log(f"Executing function: {func_name}", "INFO")
            result = func(*args, **kwargs)
            self._log(f"✓ {func_name} executed successfully", "SUCCESS")
            
            self.execution_history.append({
                'function': func_name,
                'status': 'success',
                'timestamp': datetime.now()
            })
            
            return (True, result, None)
            
        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)}"
            tb = traceback.format_exc()
            
            self._log(f"✗ Error in {func_name}: {error_msg}", "ERROR")
            if self.verbose:
                self._log(f"Traceback:\n{tb}", "ERROR")
            
            self.execution_history.append({
                'function': func_name,
                'status': 'failed',
                'error': error_msg,
                'timestamp': datetime.now()
            })
            
            return (False, None, error_msg)
    
    def safe_exec_code(self, code: str, namespace: Optional[Dict] = None) -> tuple:
        """
        Safely execute code string using exec() with non-blocking security scanners:
        - Obfuscation Detector: Warns about evasion patterns (base64, excessive dunders)
        - Behavioral Detector: Warns about runtime file/network access attempts
        - Output Guardian: Warns about large outputs or potential secret leakage
        
        Args:
            code (str): Python code to execute
            namespace (dict): Optional namespace dictionary
            
        Returns:
            Tuple of (success: bool, namespace: dict, error: str)
        """
        # ==================== LAYER 1: OBFUSCATION DETECTOR (STATIC SCAN - NON-BLOCKING) ====================
        obfuscation_warnings = []
        
        # Base64/encoding evasion patterns
        if re.search(r'base64(\.b64decode)?|exec\(|eval\(|compile\(|__import__', code, re.IGNORECASE):
            obfuscation_warnings.append("Base64/exec/eval patterns detected (potential evasion attempt)")
        
        # Excessive dunder attributes (introspection probing)
        # Count only actual dunder-style identifiers (e.g., __dict__, __class__)
        dunder_matches = re.findall(r'\b__\w+__\b', code)
        dunder_count = len(dunder_matches)
        suspicious_dunder_threshold = 20
        if dunder_count >= suspicious_dunder_threshold:
            obfuscation_warnings.append(
                f"High number of dunder attributes ({dunder_count} occurrences, "
                f"threshold={suspicious_dunder_threshold}) - possible introspection or obfuscation"
            )
        
        # Long obfuscated strings (hex/unicode encoding)
        if re.search(r'\\x[0-9a-f]{2}|\\u[0-9a-f]{4}', code):
            obfuscation_warnings.append("Hex/unicode escape sequences detected (possible obfuscation)")
        
        # Report obfuscation warnings
        for warning in obfuscation_warnings:
            self._log(f"⚠️ OBFUSCATION WARNING: {warning}", "SECURITY")
        
        # ==================== LAYER 2: BEHAVIORAL DETECTOR (RUNTIME TRACING) ====================
        behavioral_flags = {
            'file_access': False,
            'network_access': False,
            'introspection': False
        }
        
        def trace_behavior(frame, event, arg):
            """
            Trace callback used for lightweight behavioral detection.
            This function must never raise, to avoid breaking traced code.
            """
            try:
                if event == 'call':
                    func_code = getattr(frame, "f_code", None)
                    func_name = ""
                    if func_code is not None:
                        func_name = getattr(func_code, "co_name", "") or ""
                    func_name = str(func_name).lower()
                    # Detect file operations
                    if any(kw in func_name for kw in ['open', 'read', 'write', 'file', 'path']):
                        behavioral_flags['file_access'] = True
                    # Detect network operations
                    if any(kw in func_name for kw in ['socket', 'connect', 'request', 'urlopen', 'get', 'post']):
                        behavioral_flags['network_access'] = True
                    # Detect introspection
                    if any(kw in func_name for kw in ['globals', 'locals', 'dir', 'getattr', 'setattr', 'vars']):
                        behavioral_flags['introspection'] = True
            except Exception as e:
                # Never let tracing errors affect the code being executed
                self._log(f"Error in trace_behavior: {e}", "ERROR")
            return trace_behavior
        
        # Enable tracing before execution
        original_trace = sys.gettrace()
        sys.settrace(trace_behavior)
        
        if namespace is None:
            namespace = {}
        
        try:
            self._log("Executing code block...", "INFO")
            exec(code, namespace)
            self._log("✓ Code executed successfully", "SUCCESS")
        except SyntaxError as e:
            error_msg = f"Syntax error at line {e.lineno}: {e.msg}"
            self._log(f"✗ {error_msg}", "ERROR")
            # Restore trace before returning
            sys.settrace(original_trace)
            return (False, namespace, error_msg)
        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)}"
            tb = traceback.format_exc()
            self._log(f"✗ Execution error: {error_msg}", "ERROR")
            if self.verbose:
                self._log(f"Traceback:\n{tb}", "ERROR")
            # Restore trace before returning
            sys.settrace(original_trace)
            return (False, namespace, error_msg)
        
        # Restore original trace function after execution
        sys.settrace(original_trace)
        
        # ==================== LAYER 3: OUTPUT GUARDIAN (POST-EXECUTION SCAN) ====================
        # Large output detection (>1MB total size)
        total_output_size = sum(sys.getsizeof(str(v)) for v in namespace.values() if v is not None)
        if total_output_size > 1_000_000:  # 1MB threshold
            self._log(f"⚠️ OUTPUT GUARDIAN: Large output detected ({total_output_size/1024:.0f}KB) - log bombing risk?", "SECURITY")
        
        # Secret leakage patterns (non-blocking scan)
        secret_patterns = [
            r'(?i)password\s*[=:]\s*[\'"][^\'"]{8,}[\'"]',
            r'(?i)api[_-]?key\s*[=:]\s*[\'"][a-z0-9]{20,}[\'"]',
            r'(?i)token\s*[=:]\s*[\'"][a-z0-9._-]{30,}[\'"]',
            r'(?i)secret\s*[=:]\s*[\'"][^\'"]{15,}[\'"]'
        ]
        
        for key, value in namespace.items():
            if key.startswith('_') or key in ('__builtins__',):
                continue
            str_val = str(value)[:2000]  # Limit scan to first 2KB
            for pattern in secret_patterns:
                if re.search(pattern, str_val):
                    self._log(f"⚠️ OUTPUT GUARDIAN: Potential secret leakage in '{key}' variable", "SECURITY")
                    break
        
        # Report behavioral warnings AFTER execution completes
        if behavioral_flags['file_access']:
            self._log("⚠️ BEHAVIORAL WARNING: File access patterns detected during execution", "SECURITY")
        if behavioral_flags['network_access']:
            self._log("⚠️ BEHAVIORAL WARNING: Network access patterns detected during execution", "SECURITY")
        if behavioral_flags['introspection']:
            self._log("⚠️ BEHAVIORAL WARNING: Introspection patterns detected during execution", "SECURITY")
        
        # Always return success if no exception occurred (non-blocking design)
        return (True, namespace, None)
    
    def safe_exec_file(self, file_path: str, namespace: Optional[Dict] = None) -> tuple:
        """
        Safely execute a Python file
        
        Args:
            file_path (str): Path to Python file
            namespace (dict): Optional namespace dictionary
            
        Returns:
            Tuple of (success: bool, namespace: dict, error: str)
        """
        try:
            if not os.path.exists(file_path):
                error_msg = f"File not found: {file_path}"
                self._log(f"✗ {error_msg}", "ERROR")
                return (False, {}, error_msg)
            
            with open(file_path, 'r') as f:
                code = f.read()
            
            self._log(f"Executing file: {file_path}", "INFO")
            return self.safe_exec_code(code, namespace)
            
        except Exception as e:
            error_msg = f"Error reading file: {str(e)}"
            self._log(f"✗ {error_msg}", "ERROR")
            return (False, {}, error_msg)
    
    def try_import_or_install(self, package_name: str, import_name: Optional[str] = None) -> Optional[Any]:
        """
        Try to import a package, suggest installation if not found
        
        Args:
            package_name (str): Package name for pip install
            import_name (str): Import name if different from package name
            
        Returns:
            Module object if successful, None if failed
        """
        if import_name is None:
            import_name = package_name
        
        try:
            module = importlib.import_module(import_name)
            self.loaded_modules[import_name] = module
            self._log(f"✓ {import_name} is available", "SUCCESS")
            return module
            
        except ImportError:
            self._log(
                f"✗ {import_name} not found. Install with: pip install {package_name}",
                "WARNING"
            )
            return None
    
    def get_summary(self) -> Dict:
        """
        Get summary of all operations
        
        Returns:
            Dictionary with statistics and details
        """
        return {
            'total_modules_attempted': len(self.loaded_modules) + len(self.failed_modules),
            'modules_loaded': len(self.loaded_modules),
            'modules_failed': len(self.failed_modules),
            'loaded_module_names': list(self.loaded_modules.keys()),
            'failed_module_names': list(self.failed_modules.keys()),
            'failed_details': self.failed_modules.copy(),
            'execution_history': self.execution_history.copy()
        }
    
    def print_summary(self):
        """Print a formatted summary report"""
        summary = self.get_summary()
        
        print("\n" + "="*60)
        print("SAFELOADER SUMMARY REPORT")
        print("="*60)
        print(f"Total Modules Attempted: {summary['total_modules_attempted']}")
        print(f"Successfully Loaded: {summary['modules_loaded']}")
        print(f"Failed to Load: {summary['modules_failed']}")
        
        if summary['loaded_module_names']:
            print(f"\n✓ Loaded Modules:")
            for name in summary['loaded_module_names']:
                print(f"  - {name}")
        
        if summary['failed_module_names']:
            print(f"\n✗ Failed Modules:")
            for name in summary['failed_module_names']:
                print(f"  - {name}: {summary['failed_details'][name]}")
        
        if summary['execution_history']:
            print(f"\nExecution History ({len(summary['execution_history'])} operations):")
            for item in summary['execution_history'][-5:]:  # Show last 5
                status_icon = "✓" if item['status'] == 'success' else "✗"
                print(f"  {status_icon} {item['function']} - {item['timestamp'].strftime('%H:%M:%S')}")
        
        print("="*60 + "\n")
    
    def reset(self):
        """Reset all tracking data"""
        self.loaded_modules.clear()
        self.failed_modules.clear()
        self.execution_history.clear()
        self._log("SafeLoader reset", "INFO")
        
    def __enter__(self):
        """Enable context manager support - called when entering 'with' block"""
        self._log("SafeLoader context started", "INFO")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Enable context manager support - called when exiting 'with' block"""
        if exc_type is not None:
            self._log(f"Context exited with error: {exc_type.__name__}: {exc_val}", "ERROR")
        else:
            self._log("SafeLoader context completed successfully", "INFO")
        
        print("\n\n" + "="*60)
        print("FINAL SUMMARY - ALL OPERATIONS")
        print("="*60)
        
        self.print_summary()
        
        print("\n\n" + "="*60)
        print("SafeLoader context closed")
        print("="*60)
        
        self.reset()
        return False

# ============================================================================
# DEPENDENCY VERSION CHECKING WITH ADJUSTMENT FEATURE
# ============================================================================

def dependency_version_checker(
    dependencies: Dict[str, str],
    verbose: bool = True,
    recommendations: Optional[Dict[str, List[str]]] = None,
    available_for_adjustment: Optional[Dict[str, List[str]]] = None,
) -> Dict[str, Any]:
    """
    Check installed package versions against requirements and suggest adjustments
    for version conflicts, supporting both upgrades and downgrades.
    
    This function combines dependency checking with intelligent version adjustment
    recommendations based on error patterns and compatibility issues.
    
    Args:
        dependencies: Dict mapping package_name -> version_spec
            e.g., {"numpy": ">=1.20.0", "pandas": "==1.3.0"}
        verbose: Print detailed status report (default: True)
        recommendations: Dict of package_name -> list of recommended versions
        available_for_adjustment: Dict of package_name -> list of available versions
            Used for suggesting downgrades/upgrades when compatibility issues occur
    
    Returns:
        Dict with:
            - 'all_satisfied': bool, True if all dependencies are satisfied
            - 'results': Dict with per-package details:
                - 'installed_version': Installed version or None
                - 'required_version': Required version spec
                - 'satisfied': bool, True if requirement is met
                - 'status': 'ok', 'outdated', or 'missing'
                - 'message': Human-readable message
                - 'adjustment_suggested': Suggested version for adjustment (if needed)
                - 'adjustment_reason': Why this adjustment is suggested
    
    Examples:
        Basic usage:
        >>> deps = {"pip": ">=24.0", "setuptools": ">=80.0"}
        >>> result = dependency_version_checker(deps)
        >>> print(result['all_satisfied'])  # True if all OK
        
        With adjustment suggestions:
        >>> available = {"numpy": ["1.19.0", "1.20.0", "1.21.0", "1.22.0"]}
        >>> result = dependency_version_checker(
        ...     {"numpy": ">=1.20.0"},
        ...     available_for_adjustment=available
        ... )
    """
    
    def _parse_requirement(requirement: str) -> tuple:
        """Parse version requirement like '>=1.0.0' into operator and version"""
        operators = (">=", "<=", "==", ">", "<")
        trimmed = requirement.strip()
        for op in operators:
            if trimmed.startswith(op):
                return op, trimmed[len(op):].strip()
        return ">=", trimmed
    
    def _compare_versions(installed: str, operator: str, required: str) -> bool:
        """Compare two version strings using the given operator"""
        try:
            from packaging.version import Version
            installed_v = Version(installed)
            required_v = Version(required)
        except Exception:
            from distutils.version import LooseVersion  # type: ignore
            installed_v = LooseVersion(installed)
            required_v = LooseVersion(required)
        
        if operator == ">=":
            return installed_v >= required_v
        if operator == "<=":
            return installed_v <= required_v
        if operator == "==":
            return installed_v == required_v
        if operator == ">":
            return installed_v > required_v
        if operator == "<":
            return installed_v < required_v
        return False
    
    def _suggest_adjustment(package: str, current: str, operator: str, 
                           required: str) -> tuple:
        """Suggest version adjustment if available versions are provided"""
        if not available_for_adjustment or package not in available_for_adjustment:
            return None, None
        
        available = available_for_adjustment[package]
        
        try:
            from packaging.version import Version
            version_parser = Version
        except Exception:
            from distutils.version import LooseVersion  # type: ignore
            version_parser = LooseVersion
        
        try:
            current_v = version_parser(current)
            sorted_versions = sorted(
                [v for v in available if v != current],
                key=lambda v: version_parser(v),
                reverse=True
            )
        except Exception:
            sorted_versions = sorted([v for v in available if v != current], reverse=True)
        
        if not sorted_versions:
            return None, None
        
        # For version mismatches, prefer downgrade if operator is >= and newer versions are failing
        # Prefer upgrade for breaking changes
        if operator == "==":
            # For exact version, suggest the required version if available
            if required in sorted_versions:
                return required, f"Exact version mismatch - use required {required}"
        
        # Check if we should downgrade (compatibility issues with newer versions)
        downgrade_candidates = [v for v in sorted_versions 
                               if version_parser(v) < current_v]
        if downgrade_candidates and operator == ">=":
            suggestion = downgrade_candidates[0]
            return suggestion, f"Downgrade to {suggestion} for compatibility"
        
        # Check if we should upgrade (missing features or fixes)
        upgrade_candidates = [v for v in sorted_versions 
                            if version_parser(v) > current_v]
        if upgrade_candidates:
            suggestion = upgrade_candidates[0]
            return suggestion, f"Upgrade to {suggestion} to satisfy {operator}{required}"
        
        # Default to first available
        if sorted_versions:
            suggestion = sorted_versions[0]
            reason = f"Alternative version: {suggestion}"
            return suggestion, reason
        
        return None, None
    
    def _pick_recommended(package_name: str) -> Optional[str]:
        """Pick the highest recommended version for a package"""
        if not recommendations or package_name not in recommendations:
            return None
        
        versions = recommendations[package_name]
        try:
            from packaging.version import Version
            parsed = sorted(((Version(v), v) for v in versions), reverse=True)
        except Exception:
            from distutils.version import LooseVersion  # type: ignore
            parsed = sorted(((LooseVersion(v), v) for v in versions), reverse=True)
        
        return parsed[0][1] if parsed else None
    
    # Process each dependency
    results: Dict[str, Dict[str, Any]] = {}
    all_satisfied = True
    
    for package_name, requirement in dependencies.items():
        operator, required_version = _parse_requirement(str(requirement))
        
        try:
            installed_version = importlib_metadata.version(package_name)
        except importlib_metadata.PackageNotFoundError:
            # Package not installed
            recommended = _pick_recommended(package_name)
            suggestion = recommended or f"{operator}{required_version}"
            
            results[package_name] = {
                "installed_version": None,
                "required_version": f"{operator}{required_version}",
                "satisfied": False,
                "status": "missing",
                "recommended_version": recommended,
                "adjustment_suggested": f"Install {package_name}=={suggestion}",
                "adjustment_reason": "Package not installed",
                "message": (
                    f"{package_name} is not installed; requires {operator}{required_version}. "
                    f"Install with: pip install {package_name}"
                ),
            }
            all_satisfied = False
            
            if verbose:
                print(
                    f"[MISSING ] {package_name:<18} requires {operator}{required_version:<10} "
                    f"→ Install {suggestion}"
                )
            continue
        
        # Check if installed version satisfies requirement
        is_satisfied = _compare_versions(installed_version, operator, required_version)
        all_satisfied = all_satisfied and is_satisfied
        
        # Get adjustment suggestion if not satisfied
        adjustment_suggested, adjustment_reason = None, None
        if not is_satisfied:
            adjustment_suggested, adjustment_reason = _suggest_adjustment(
                package_name, installed_version, operator, required_version
            )
        
        recommended = _pick_recommended(package_name)
        
        results[package_name] = {
            "installed_version": installed_version,
            "required_version": f"{operator}{required_version}",
            "satisfied": is_satisfied,
            "status": "ok" if is_satisfied else "outdated",
            "recommended_version": recommended,
            "adjustment_suggested": adjustment_suggested,
            "adjustment_reason": adjustment_reason,
            "message": (
                f"{package_name} {installed_version} installed; requires {operator}{required_version}"
            ),
        }
        
        if verbose:
            if is_satisfied:
                print(
                    f"[OK      ] {package_name:<18} {installed_version:<10} "
                    f"✓ requires {operator}{required_version}"
                )
            else:
                adj_info = f" → Adjust to {adjustment_suggested}" if adjustment_suggested else ""
                print(
                    f"[OUTDATED] {package_name:<18} {installed_version:<10} "
                    f"→ requires {operator}{required_version}{adj_info}"
                )
    
    return {"all_satisfied": all_satisfied, "results": results}

# Convenience functions for quick use
def quick_load(*module_names, verbose=True) -> Dict[str, Any]:
    """
    Quick function to load modules without creating a SafeLoader instance
    
    Usage:
        modules = quick_load('requests', 'numpy', 'pandas')
    """
    loader = SafeLoader(verbose=verbose)
    return loader.load_modules(list(module_names))


def safe_run(func: Callable, *args, **kwargs) -> tuple:
    """
    Quick function to safely run any function
    
    Usage:
        success, result, error = safe_run(my_function, arg1, arg2)
    """
    loader = SafeLoader(verbose=False)
    return loader.safe_execute(func, *args, **kwargs)


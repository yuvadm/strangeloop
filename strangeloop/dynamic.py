"""
Dynamic code loading and execution module for Strangeloop.
Provides functionality to dynamically add code to the running instance.
"""
import importlib.util
import sys
import types
import inspect
from pathlib import Path
from typing import Any, Dict, Optional, Callable


def add_function_to_module(module_name: str, function_code: str, function_name: Optional[str] = None) -> Callable:
    """
    Dynamically add a function to a module in the current Python process.
    
    Args:
        module_name: The name of the module to add the function to
        function_code: The Python code for the function
        function_name: Optional name to extract from the function code
                      (if None, will try to parse from the code)
    
    Returns:
        The function object that was added
    
    Raises:
        ValueError: If function_name cannot be determined or module doesn't exist
        SyntaxError: If the function code has syntax errors
    """
    # Get the module
    if module_name not in sys.modules:
        raise ValueError(f"Module '{module_name}' not found in sys.modules")
    
    module = sys.modules[module_name]
    
    # Create a new namespace for executing the function code
    namespace: Dict[str, Any] = {}
    
    # Execute the function code in the namespace
    try:
        exec(function_code, namespace)
    except SyntaxError as e:
        raise SyntaxError(f"Syntax error in function code: {str(e)}")
    
    # If function_name is not provided, try to extract it from the code
    if function_name is None:
        # Look for function definitions in the namespace
        functions = [name for name, obj in namespace.items() 
                    if inspect.isfunction(obj)]
        
        if not functions:
            raise ValueError("No function found in the provided code")
        
        function_name = functions[0]
    
    # Get the function from the namespace
    if function_name not in namespace:
        raise ValueError(f"Function '{function_name}' not found in the provided code")
    
    function = namespace[function_name]
    
    # Add the function to the module
    setattr(module, function_name, function)
    
    return function


def save_function_to_file(function_code: str, directory: Optional[Path] = None) -> Path:
    """
    Save a dynamically created function to a file in the capabilities directory.
    
    Args:
        function_code: The Python code for the function
        directory: Optional directory to save the file (defaults to capabilities)
    
    Returns:
        Path to the saved file
    """
    # Extract function name from the code
    import re
    match = re.search(r"def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", function_code)
    if not match:
        raise ValueError("Could not extract function name from code")
    
    function_name = match.group(1)
    
    # Determine the directory to save the file
    if directory is None:
        # Get the strangeloop package directory
        package_dir = Path(__file__).parent
        directory = package_dir / "capabilities"
    
    # Create the directory if it doesn't exist
    directory.mkdir(parents=True, exist_ok=True)
    
    # Create the file path
    file_path = directory / f"{function_name}.py"
    
    # Add module docstring if not present
    if not function_code.strip().startswith('"""'):
        function_code = f'"""\nDynamically generated capability: {function_name}\n"""\n\n{function_code}'
    
    # Write the function code to the file
    with open(file_path, "w") as f:
        f.write(function_code)
    
    return file_path

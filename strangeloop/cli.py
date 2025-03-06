#!/usr/bin/env python
"""
Strangeloop CLI - A recursive and self-referential AI agent framework.
"""
import click
import sys
import json
import importlib
import inspect
import textwrap
from pathlib import Path
from typing import Dict, Any, List, Callable, Optional, Tuple
from .llm import ask_claude
from .config import get_config


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Strangeloop - A recursive and self-referential AI agent framework."""
    pass


@cli.command()
def hello():
    """Print a hello message."""
    click.echo("Hello from strangeloop!")


@cli.command()
@click.argument("name", required=False)
def greet(name=None):
    """Greet a user by name."""
    if name:
        click.echo(f"Hello, {name}! Welcome to strangeloop!")
    else:
        click.echo("Hello! Welcome to strangeloop!")


@cli.command()
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
def info(verbose):
    """Display information about the strangeloop environment."""
    click.echo("Strangeloop Information:")
    click.echo(f"Python version: {sys.version}")
    click.echo(f"Running from: {Path(__file__).resolve().parent}")
    
    if verbose:
        click.echo("\nVerbose Information:")
        click.echo(f"Platform: {sys.platform}")
        click.echo(f"Python executable: {sys.executable}")


@cli.command()
@click.argument("file_path", type=click.Path(exists=True))
@click.option("--output", "-o", help="Output file path")
def process(file_path, output):
    """Process a file with strangeloop."""
    click.echo(f"Processing file: {file_path}")
    
    # This is a placeholder for actual processing logic
    click.echo("Processing complete!")
    
    if output:
        click.echo(f"Results written to: {output}")


@cli.command()
@click.argument("question", required=True)
@click.option("--max-tokens", "-m", default=1024, help="Maximum tokens in response")
@click.option("--temperature", "-t", default=0.7, type=float, help="Temperature (0.0-1.0)")
def ask(question, max_tokens, temperature):
    """Ask Claude Sonnet 3.7 a question and get a response."""
    try:
        click.echo("Asking Claude Sonnet 3.7...")
        response = ask_claude(question, max_tokens, temperature)
        click.echo("\nResponse:")
        click.echo(response)
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@cli.group()
def capability():
    """Manage strangeloop capabilities."""
    pass


@capability.command(name="add")
@click.argument("description", required=True)
@click.option("--max-tokens", "-m", default=4096, help="Maximum tokens in response")
@click.option("--temperature", "-t", default=0.5, type=float, help="Temperature (0.0-1.0)")
@click.option("--save/--no-save", "-s/-n", default=True, help="Save the function to a file (default: save)")
def capability_add(description, max_tokens, temperature, save):
    """
    Add a new capability using Claude and dynamically add it to strangeloop.
    
    DESCRIPTION is a description of what the function should do.
    """
    try:
        from .dynamic import add_function_to_module, save_function_to_file
        import strangeloop
        
        # Prepare the prompt for Claude
        prompt = f"""
        Implement a Python function based on this capability description:
        
        {description}
        
        Requirements:
        1. Write a single, well-documented Python function with clear docstrings
        2. Include proper type hints
        3. Include appropriate error handling
        4. Make the function name descriptive of its purpose
        5. Only return the function code, nothing else
        """
        
        click.echo(f"Asking Claude to implement: {description}")
        function_code = ask_claude(prompt, max_tokens, temperature)
        
        # Clean up the response if needed (remove markdown code blocks)
        function_code = function_code.strip()
        if function_code.startswith("```python"):
            function_code = function_code[len("```python"):].strip()
        if function_code.startswith("```"):
            function_code = function_code[len("```"):].strip()
        if function_code.endswith("```"):
            function_code = function_code[:-len("```")].strip()
        
        # Display the generated function
        click.echo("\nGenerated function:")
        click.echo(function_code)
        
        # Add the function to the strangeloop module
        try:
            function = add_function_to_module("strangeloop", function_code)
            function_name = function.__name__
            click.echo(f"\nSuccessfully added function '{function_name}' to strangeloop")
            
            # Save the function to a file if requested
            if save:
                file_path = save_function_to_file(function_code)
                click.echo(f"Saved function to {file_path}")
                
                # Add import to __init__.py to make it available in future sessions
                capabilities_init = Path(__file__).parent / "capabilities" / "__init__.py"
                with open(capabilities_init, "a") as f:
                    f.write(f"\nfrom strangeloop.capabilities.{function_name} import {function_name}\n")
                
                click.echo(f"Added import to capabilities/__init__.py for future sessions")
            
            # Show usage example
            click.echo("\nUsage example:")
            click.echo(f"  from strangeloop import {function_name}")
            click.echo(f"  help({function_name})  # View documentation")
            click.echo(f"  # Or use the CLI:")
            click.echo(f"  strangeloop capability run {function_name} [ARGS...]")
            
        except Exception as e:
            click.echo(f"Error adding function to strangeloop: {str(e)}", err=True)
            sys.exit(1)
            
    except Exception as e:
        click.echo(f"Error implementing capability: {str(e)}", err=True)
        sys.exit(1)


@capability.command(name="list")
@click.option("--verbose", "-v", is_flag=True, help="Show detailed information about each capability")
def capability_list(verbose):
    """List all available capabilities."""
    try:
        # Import capabilities module
        try:
            import strangeloop.capabilities as capabilities
            importlib.reload(capabilities)  # Reload to catch any new capabilities
        except ImportError:
            click.echo("No capabilities found.")
            return
        
        # Get all functions from the capabilities module
        functions = []
        for name in dir(capabilities):
            if name.startswith('_'):
                continue
            
            obj = getattr(capabilities, name)
            if inspect.isfunction(obj):
                functions.append((name, obj))
        
        if not functions:
            click.echo("No capabilities found.")
            return
        
        click.echo(f"Found {len(functions)} capabilities:")
        for name, func in sorted(functions, key=lambda x: x[0]):
            if verbose:
                # Get the first line of the docstring
                doc = inspect.getdoc(func) or "No documentation"
                doc_first_line = doc.split('\n')[0]
                
                # Get the function signature
                sig = str(inspect.signature(func))
                
                click.echo(f"\n{name}{sig}")
                click.echo(f"  {doc_first_line}")
                
                # Show file location
                try:
                    file_path = inspect.getfile(func)
                    click.echo(f"  Defined in: {file_path}")
                except (TypeError, OSError):
                    pass
            else:
                click.echo(f"- {name}")
        
        if not verbose:
            click.echo("\nUse --verbose for more details.")
            click.echo("Use 'strangeloop capability show <name>' to see full documentation.")
    
    except Exception as e:
        click.echo(f"Error listing capabilities: {str(e)}", err=True)
        sys.exit(1)


@capability.command(name="show")
@click.argument("name", required=True)
def capability_show(name):
    """Show detailed information about a specific capability."""
    try:
        # Import capabilities module
        try:
            import strangeloop.capabilities as capabilities
            importlib.reload(capabilities)  # Reload to catch any new capabilities
        except ImportError:
            click.echo("No capabilities found.")
            return
        
        # Get the function
        if not hasattr(capabilities, name):
            click.echo(f"Capability '{name}' not found.")
            return
        
        func = getattr(capabilities, name)
        if not inspect.isfunction(func):
            click.echo(f"'{name}' is not a function capability.")
            return
        
        # Display function information
        click.echo(f"Capability: {name}{inspect.signature(func)}")
        
        # Show docstring
        doc = inspect.getdoc(func) or "No documentation"
        click.echo("\nDocumentation:")
        click.echo(doc)
        
        # Show source code
        try:
            source = inspect.getsource(func)
            click.echo("\nSource Code:")
            click.echo(source)
        except (TypeError, OSError) as e:
            click.echo(f"\nCould not retrieve source code: {str(e)}")
        
        # Show file location
        try:
            file_path = inspect.getfile(func)
            click.echo(f"\nDefined in: {file_path}")
        except (TypeError, OSError):
            pass
        
        # Show usage example
        click.echo("\nUsage example:")
        click.echo(f"  from strangeloop import {name}")
        click.echo(f"  result = {name}(...)")
        click.echo(f"  # Or use the CLI:")
        click.echo(f"  strangeloop capability run {name} [ARGS...]")
    
    except Exception as e:
        click.echo(f"Error showing capability: {str(e)}", err=True)
        sys.exit(1)


@capability.command(name="run")
@click.argument("name", required=True)
@click.argument("args", nargs=-1)
@click.option("--json", "-j", is_flag=True, help="Parse arguments as JSON")
def capability_run(name, args, json):
    """
    Run a capability with the given arguments.
    
    NAME is the name of the capability to run.
    ARGS are the arguments to pass to the capability.
    """
    try:
        # Import capabilities module
        try:
            import strangeloop.capabilities as capabilities
            importlib.reload(capabilities)  # Reload to catch any new capabilities
        except ImportError:
            click.echo("No capabilities found.")
            return
        
        # Get the function
        if not hasattr(capabilities, name):
            click.echo(f"Capability '{name}' not found.")
            return
        
        func = getattr(capabilities, name)
        if not inspect.isfunction(func):
            click.echo(f"'{name}' is not a function capability.")
            return
        
        # Parse arguments
        parsed_args = []
        parsed_kwargs = {}
        
        if json:
            # Parse all arguments as JSON
            import json as json_module
            for arg in args:
                try:
                    parsed_args.append(json_module.loads(arg))
                except json_module.JSONDecodeError:
                    # If not valid JSON, use as string
                    parsed_args.append(arg)
        else:
            # Simple string arguments
            parsed_args = args
        
        # Run the function
        click.echo(f"Running capability '{name}'...")
        result = func(*parsed_args, **parsed_kwargs)
        
        # Display the result
        click.echo("\nResult:")
        if result is None:
            click.echo("(No return value)")
        elif isinstance(result, (dict, list)):
            click.echo(json.dumps(result, indent=2))
        else:
            click.echo(result)
    
    except Exception as e:
        click.echo(f"Error running capability: {str(e)}", err=True)
        sys.exit(1)


@cli.group()
def config():
    """Manage Strangeloop configuration."""
    pass


@config.command(name="set")
@click.argument("key", required=True)
@click.argument("value", required=True)
def config_set(key, value):
    """Set a configuration value."""
    try:
        # Try to parse as JSON if possible
        try:
            value = json.loads(value)
        except json.JSONDecodeError:
            # If not valid JSON, use as string
            pass
        
        config = get_config()
        config.set(key, value)
        click.echo(f"Configuration '{key}' set to: {value}")
    except Exception as e:
        click.echo(f"Error setting configuration: {str(e)}", err=True)
        sys.exit(1)


@config.command(name="get")
@click.argument("key", required=True)
def config_get(key):
    """Get a configuration value."""
    try:
        config = get_config()
        value = config.get(key)
        if value is None:
            click.echo(f"Configuration '{key}' is not set")
        else:
            if isinstance(value, (dict, list)):
                click.echo(json.dumps(value, indent=2))
            else:
                click.echo(value)
    except Exception as e:
        click.echo(f"Error getting configuration: {str(e)}", err=True)
        sys.exit(1)


@config.command(name="list")
def config_list():
    """List all configuration values."""
    try:
        config = get_config()
        values = config.list_all()
        if not values:
            click.echo("No configuration values set")
        else:
            click.echo(json.dumps(values, indent=2))
    except Exception as e:
        click.echo(f"Error listing configuration: {str(e)}", err=True)
        sys.exit(1)


@config.command(name="delete")
@click.argument("key", required=True)
def config_delete(key):
    """Delete a configuration value."""
    try:
        config = get_config()
        if config.delete(key):
            click.echo(f"Configuration '{key}' deleted")
        else:
            click.echo(f"Configuration '{key}' not found")
    except Exception as e:
        click.echo(f"Error deleting configuration: {str(e)}", err=True)
        sys.exit(1)


@config.command(name="path")
def config_path():
    """Show the configuration file path."""
    try:
        config = get_config()
        click.echo(f"Configuration directory: {config.config_dir}")
        click.echo(f"Configuration file: {config.config_file}")
    except Exception as e:
        click.echo(f"Error getting configuration path: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("request", required=True, nargs=-1)
@click.option("--max-tokens", "-m", default=4096, help="Maximum tokens in response")
@click.option("--temperature", "-t", default=0.7, type=float, help="Temperature (0.0-1.0)")
@click.option("--auto-execute/--no-auto-execute", default=True, help="Automatically execute the suggested action")
def do(request, max_tokens, temperature, auto_execute):
    """
    Execute an AI agent loop to fulfill a request using available capabilities.
    
    REQUEST is what you want strangeloop to do for you.
    """
    try:
        # Convert request tuple to string
        request_str = " ".join(request)
        click.echo(f"Processing request: {request_str}")
        
        # Get available capabilities
        capabilities_info = get_available_capabilities()
        
        if not capabilities_info:
            click.echo("No capabilities available. Creating a new capability...")
            if auto_execute:
                click.echo("Automatically creating a new capability to handle your request.")
                ctx = click.get_current_context()
                return ctx.invoke(capability_add, description=request_str, 
                                max_tokens=max_tokens, temperature=temperature, save=True)
            else:
                click.echo("Use 'strangeloop capability add' to create a new capability.")
                return
        
        # Format capabilities for the prompt
        capabilities_text = format_capabilities_for_prompt(capabilities_info)
        
        # Prepare the prompt for Claude
        prompt = f"""
        # Request
        The user has requested: "{request_str}"
        
        # Available Capabilities
        You have the following capabilities available:
        
        {capabilities_text}
        
        # Your Task
        Analyze the request and determine the best course of action:
        
        1. If an existing capability can handle the request (or part of it), respond with a JSON object like this:
           {{
             "action": "use_capability",
             "capability": "capability_name",
             "arguments": ["arg1", "arg2", ...],
             "explanation": "Why this capability is appropriate"
           }}
        
        2. If the request requires a new capability, respond with a JSON object like this:
           {{
             "action": "create_capability",
             "description": "Detailed description of the capability needed",
             "explanation": "Why a new capability is needed"
           }}
        
        3. If the request can be answered directly without using or creating capabilities, respond with:
           {{
             "action": "direct_response",
             "response": "Your detailed response to the request",
             "explanation": "Why a direct response is sufficient"
           }}
        
        Respond ONLY with a valid JSON object matching one of these formats. Do not include any other text.
        """
        
        click.echo("Consulting Claude to determine the best approach...")
        response = ask_claude(prompt, max_tokens, temperature)
        
        # Parse the JSON response
        try:
            # Clean up the response if needed (remove markdown code blocks)
            response = response.strip()
            if response.startswith("```json"):
                response = response[len("```json"):].strip()
            if response.startswith("```"):
                response = response[len("```"):].strip()
            if response.endswith("```"):
                response = response[:-len("```")].strip()
            
            action_plan = json.loads(response)
            
            # Display the explanation
            if "explanation" in action_plan:
                click.echo(f"\nReasoning: {action_plan['explanation']}")
            
            # Execute the appropriate action
            action = action_plan.get("action")
            
            if action == "use_capability":
                capability_name = action_plan.get("capability")
                arguments = action_plan.get("arguments", [])
                
                click.echo(f"\nSuggested action: Use capability '{capability_name}' with arguments: {arguments}")
                
                if auto_execute:
                    click.echo("Automatically executing the suggested capability...")
                    ctx = click.get_current_context()
                    return ctx.invoke(capability_run, name=capability_name, args=arguments, json=False)
                else:
                    click.echo("\nTo execute this capability, run:")
                    args_str = " ".join([f'"{arg}"' for arg in arguments])
                    click.echo(f"  strangeloop capability run {capability_name} {args_str}")
            
            elif action == "create_capability":
                description = action_plan.get("description")
                
                click.echo(f"\nSuggested action: Create a new capability with description:")
                click.echo(f"  {description}")
                
                if auto_execute:
                    click.echo("Automatically creating the suggested capability...")
                    ctx = click.get_current_context()
                    return ctx.invoke(capability_add, description=description, 
                                    max_tokens=max_tokens, temperature=temperature, save=True)
                else:
                    click.echo("\nTo create this capability, run:")
                    click.echo(f'  strangeloop capability add "{description}"')
            
            elif action == "direct_response":
                direct_response = action_plan.get("response", "")
                
                click.echo("\nDirect response:")
                click.echo(textwrap.fill(direct_response, width=80))
            
            else:
                click.echo(f"\nUnknown action type: {action}")
                click.echo("Full response from Claude:")
                click.echo(response)
        
        except json.JSONDecodeError:
            click.echo("Could not parse Claude's response as JSON. Full response:")
            click.echo(response)
            sys.exit(1)
    
    except Exception as e:
        click.echo(f"Error processing request: {str(e)}", err=True)
        sys.exit(1)


def get_available_capabilities() -> List[Dict[str, Any]]:
    """
    Get information about all available capabilities.
    
    Returns:
        List of dictionaries with capability information
    """
    capabilities_info = []
    
    try:
        # Import capabilities module
        try:
            import strangeloop.capabilities as capabilities
            importlib.reload(capabilities)  # Reload to catch any new capabilities
        except ImportError:
            return capabilities_info
        
        # Get all functions from the capabilities module
        for name in dir(capabilities):
            if name.startswith('_'):
                continue
            
            obj = getattr(capabilities, name)
            if inspect.isfunction(obj):
                # Get function signature
                sig = inspect.signature(obj)
                
                # Get docstring
                doc = inspect.getdoc(obj) or "No documentation"
                
                # Add to capabilities list
                capabilities_info.append({
                    "name": name,
                    "signature": str(sig),
                    "docstring": doc,
                    "parameters": [
                        {
                            "name": param_name,
                            "annotation": str(param.annotation) if param.annotation != inspect.Parameter.empty else "Any",
                            "default": None if param.default == inspect.Parameter.empty else param.default,
                            "required": param.default == inspect.Parameter.empty and param.kind not in (
                                inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD)
                        }
                        for param_name, param in sig.parameters.items()
                    ]
                })
    
    except Exception as e:
        click.echo(f"Warning: Error getting capabilities: {str(e)}", err=True)
    
    return capabilities_info


def format_capabilities_for_prompt(capabilities_info: List[Dict[str, Any]]) -> str:
    """
    Format capabilities information for inclusion in a prompt.
    
    Args:
        capabilities_info: List of dictionaries with capability information
    
    Returns:
        Formatted string describing capabilities
    """
    if not capabilities_info:
        return "No capabilities available."
    
    formatted_text = ""
    
    for cap in capabilities_info:
        # Format the first line of the docstring
        doc_first_line = cap["docstring"].split('\n')[0]
        
        # Format the capability
        formatted_text += f"- {cap['name']}{cap['signature']}\n"
        formatted_text += f"  Description: {doc_first_line}\n"
        
        # Add parameter details
        if cap["parameters"]:
            formatted_text += "  Parameters:\n"
            for param in cap["parameters"]:
                required = " (required)" if param["required"] else ""
                default = f" (default: {param['default']})" if param["default"] is not None else ""
                formatted_text += f"    - {param['name']}: {param['annotation']}{required}{default}\n"
        
        formatted_text += "\n"
    
    return formatted_text.strip()


if __name__ == "__main__":
    cli()

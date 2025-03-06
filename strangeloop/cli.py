#!/usr/bin/env python
"""
Strangeloop CLI - A recursive and self-referential AI agent framework.
"""
import click
import sys
import json
from pathlib import Path
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


if __name__ == "__main__":
    cli()

#!/usr/bin/env python
"""
Strangeloop CLI - A recursive and self-referential AI agent framework.
"""
import click
import sys
from pathlib import Path


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


if __name__ == "__main__":
    cli()

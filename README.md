# Strangeloop

A recursive and self-referential AI agent framework.

## Installation

Run the latest version directly without installation from `uvx`:

```bash
$ uvx strangeloop
```

For developers, from within working copy run:

```bash
$ uv run strangeloop
```

## CLI Usage

Strangeloop provides a command-line interface with several commands:

```bash
# Run the CLI ad hoc without installation
uvx strangeloop --help
uvx strangeloop hello
uvx strangeloop greet [NAME]
uvx strangeloop info
uvx strangeloop process FILE_PATH [--output OUTPUT_PATH]

# Ask Claude Sonnet 3.7 a question
uvx strangeloop ask "What is recursive self-improvement in AI?"

# Configuration management
uvx strangeloop config set api_key "your-api-key"
uvx strangeloop config get api_key
uvx strangeloop config list
uvx strangeloop config delete api_key
uvx strangeloop config path
```

If you've installed the package:
```bash
# Using the installed CLI
strangeloop --help
strangeloop hello
strangeloop greet [NAME]
strangeloop info
strangeloop ask "What is the meaning of life?" --max-tokens 2048 --temperature 0.8
```

## Environment Variables

The following environment variables are required:

- `ANTHROPIC_API_KEY`: Your Anthropic API key for accessing Claude Sonnet 3.7

## Configuration

Strangeloop uses the XDG Base Directory Specification for storing configuration. The configuration file is stored at:

- Linux/macOS: `~/.config/strangeloop/config.json` (or `$XDG_CONFIG_HOME/strangeloop/config.json` if set)
- Windows: `%APPDATA%\strangeloop\config.json`

You can manage configuration using the `config` command:

```bash
# Set a configuration value
strangeloop config set model "claude-3-opus-20240229"

# Get a configuration value
strangeloop config get model

# List all configuration values
strangeloop config list

# Delete a configuration value
strangeloop config delete model

# Show the configuration file path
strangeloop config path

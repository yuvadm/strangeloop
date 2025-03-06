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
uvx strangeloop config set anthropic_api_key "your-api-key"
uvx strangeloop config get anthropic_api_key
uvx strangeloop config list
uvx strangeloop config delete anthropic_api_key
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

## API Keys and Configuration

To use the Claude Sonnet 3.7 integration, you need to provide your Anthropic API key in one of these ways (in order of precedence):

1. Set in configuration:
   ```bash
   strangeloop config set anthropic_api_key "your-api-key"
   ```

2. Set as environment variable:
   ```bash
   export ANTHROPIC_API_KEY="your-api-key"
   ```

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
```

### Common Configuration Options

- `anthropic_api_key`: Your Anthropic API key

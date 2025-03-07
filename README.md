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
strangeloop --help
strangeloop hello
strangeloop greet [NAME]
strangeloop info
strangeloop process FILE_PATH [--output OUTPUT_PATH]

# Ask Claude Sonnet 3.7 a question
strangeloop ask "What is recursive self-improvement in AI?"

# Use the AI agent loop to fulfill requests
strangeloop do "find the current weather in New York"
strangeloop do "create a function to generate secure passwords"

# Manage capabilities
strangeloop capability add "generate a secure random password"
strangeloop capability list
strangeloop capability show generate_secure_password
strangeloop capability run generate_secure_password 16 --include-special-chars

# Configuration management
strangeloop config set anthropic_api_key "your-api-key"
strangeloop config get anthropic_api_key
strangeloop config list
strangeloop config delete anthropic_api_key
strangeloop config path
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

## AI Agent Loop

The core of Strangeloop is the AI agent loop, which allows you to make requests in natural language and have the system determine the best way to fulfill them:

```bash
strangeloop do "find information about the weather in Paris"
```

The system will:
1. Analyze your request
2. Check available capabilities
3. Either:
   - Use an existing capability
   - Create a new capability
   - Provide a direct response

You can control the execution with options:
```bash
# Don't automatically execute the suggested action
strangeloop do "analyze this log file" --no-auto-execute

# Adjust the temperature for more creative responses
strangeloop do "write a poem about AI" --temperature 0.9
```

## Capabilities Management

Strangeloop allows you to create, manage, and execute capabilities - Python functions that can be dynamically added to the system:

### Adding Capabilities

```bash
# Add a new capability
strangeloop capability add "generate a secure random password"

# Control the generation parameters
strangeloop capability add "fetch current weather for a location" --temperature 0.5 --max-tokens 4096
```

### Listing and Viewing Capabilities

```bash
# List all available capabilities
strangeloop capability list

# Get detailed information about capabilities
strangeloop capability list --verbose

# Show details of a specific capability
strangeloop capability show generate_secure_password
```

### Running Capabilities

```bash
# Run a capability with arguments
strangeloop capability run generate_secure_password 16 true

# Parse arguments as JSON
strangeloop capability run fetch_weather "New York" --json
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

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
# Display help
strangeloop --help

# Print a hello message
strangeloop hello

# Greet a user
strangeloop greet [NAME]

# Display information about the environment
strangeloop info
strangeloop info --verbose

# Process a file
strangeloop process FILE_PATH [--output OUTPUT_PATH]
```

You can also run the CLI directly without installation:

```bash
python main.py --help

# MCP LLM Server

A Model Context Protocol (MCP) server that provides tools to interact with Claude and Gemini CLI tools. This server enables seamless integration between MCP-compatible clients and command-line interfaces for Claude and Gemini LLMs.

## Overview

This MCP server acts as a bridge between MCP clients and the Claude and Gemini command-line interfaces. It exposes three main tools that allow you to send prompts to these LLMs and receive responses through the standardized MCP protocol.

## Prerequisites

- Python 3.10 or higher
- [Claude CLI](https://github.com/anthropics/claude-cli) installed and configured
- [Gemini CLI](https://github.com/google/gemini-cli) installed and configured
- `uv` package manager

## Installation

```bash
# Clone the repository
git clone https://github.com/straygizmo/mcp_llm_cli
cd mcp_llm_cli

# Install dependencies using uv
uv sync
```

## Usage

### Configuration for MCP Clients

To use this server with an MCP client (like Claude Desktop), add it to your MCP configuration file:

```json
{
  "mcpServers": {
    "llm-server": {
      "command": "uv",
      "args": ["run", "python", "-m", "mcp_llm_server.server"],
      "cwd": "/path/to/mcp-llm-cli"
    }
  }
}
```

## Available Tools

The server provides three tools for interacting with LLMs:

### 1. `claude_prompt`
Send a prompt to Claude and receive a response.

**Parameters:**
- `prompt` (string, required): The prompt to send to Claude

**Example:**
```json
{
  "name": "claude_prompt",
  "arguments": {
    "prompt": "Explain quantum computing in simple terms"
  }
}
```

### 2. `gemini_prompt`
Send a prompt to Gemini and receive a response.

**Parameters:**
- `prompt` (string, required): The prompt to send to Gemini

**Example:**
```json
{
  "name": "gemini_prompt",
  "arguments": {
    "prompt": "What are the benefits of renewable energy?"
  }
}
```

### 3. `llm_prompt`
Send a prompt to both Claude and Gemini simultaneously and receive both responses.

**Parameters:**
- `prompt` (string, required): The prompt to send to both LLMs

**Example:**
```json
{
  "name": "llm_prompt",
  "arguments": {
    "prompt": "Compare and contrast machine learning and deep learning"
  }
}
```

The response will include both Claude's and Gemini's answers in a formatted output.

## Architecture

The server is built using the Model Context Protocol (MCP) framework and consists of:

- **Main Server (`server.py`)**: Handles MCP protocol communication and tool execution
- **Async subprocess execution**: Calls Claude and Gemini CLIs asynchronously
- **Error handling**: Gracefully handles missing CLI tools and execution errors

## Development

### Project Structure

```
mcp-llm-cli/
├── README.md
├── pyproject.toml
├── uv.lock
└── src/
    └── mcp_llm_server/
        ├── __init__.py
        └── server.py
```

### Running in Development

For development, you can run the server with logging enabled:

```bash
uv run -m mcp_llm_server.server
```

## Error Handling

The server handles various error scenarios:
- Missing CLI tools (claude or gemini-cli not installed)
- CLI execution errors
- Invalid tool names
- Malformed requests

All errors are returned as formatted text responses to maintain compatibility with MCP clients.

## License

[Specify your license here]

## Contributing

[Add contribution guidelines if applicable]

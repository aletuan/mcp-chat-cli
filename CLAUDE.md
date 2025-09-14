# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Setup and Running
- Install dependencies: `uv pip install -e .` (recommended) or `pip install anthropic python-dotenv prompt-toolkit "mcp[cli]==1.8.0"`
- Create virtual environment: `uv venv` then `source .venv/bin/activate`
- Run application: `uv run main.py` or `python main.py`
- Run with additional MCP servers: `python main.py server1.py server2.py`

### Environment Configuration
- Required: `ANTHROPIC_API_KEY` in `.env` file
- Optional: `CLAUDE_MODEL` in `.env` file
- Optional: `USE_UV=1` to force uv usage for MCP server execution

## Architecture Overview

### Core Application Structure
This is an MCP (Model Control Protocol) chat application that enables interactive AI conversations with document retrieval and command capabilities.

**Main Components:**
- `main.py`: Entry point, orchestrates MCP clients and starts CLI
- `core/cli_chat.py`: Chat implementation with document and command processing
- `core/cli.py`: CLI interface with auto-completion and command suggestions
- `mcp_client.py`: MCP client wrapper (contains TODO placeholders for full implementation)
- `mcp_server.py`: Basic MCP server with document storage (incomplete, needs implementation)

### Key Architecture Patterns

**MCP Integration:**
- Application connects to MCP servers via stdio transport
- Default server (`mcp_server.py`) provides document access
- Additional servers can be specified as command line arguments
- Client-server communication handles prompts, tools, and resources

**Chat Flow:**
1. `CliChat` processes user input for commands (/) or document mentions (@)
2. Document mentions (@docname) automatically include content in context
3. Commands (/) trigger MCP prompts with document parameters
4. Regular queries are enhanced with mentioned document content

**CLI Features:**
- Tab completion for MCP commands and document names
- Command auto-suggestion based on available MCP prompts
- In-memory history for previous queries

### Incomplete Implementation Areas

The codebase has several TODO markers in critical areas:

**mcp_client.py:** All MCP protocol methods are stubbed (list_tools, call_tool, list_prompts, get_prompt, read_resource)

**mcp_server.py:** Missing implementations for:
- Document reading/editing tools
- Document listing resource
- Document content resource
- Markdown conversion and summarization prompts

### Development Notes

- No linting or type checking currently implemented
- Python 3.10+ required
- Uses FastMCP for server implementation
- Uses prompt-toolkit for rich CLI experience
- Async/await throughout for concurrent MCP connections
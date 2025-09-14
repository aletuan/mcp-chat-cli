# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Setup and Running
- Install dependencies: `uv pip install -e .` (recommended) or `pip install anthropic python-dotenv prompt-toolkit "mcp[cli]==1.8.0"`
- Create virtual environment: `uv venv` then `source .venv/bin/activate`
- Run application: `uv run main.py` or `python main.py`
- Run with additional MCP servers: `python main.py server1.py server2.py`

### Environment Configuration
- Required: `ANTHROPIC_API_KEY` - Your Anthropic API key from console.anthropic.com
- Required: `CLAUDE_MODEL` - Anthropic model to use (e.g., "claude-3-5-sonnet-20241022")
- Optional: `USE_UV=1` to force uv usage for MCP server execution

## Architecture Overview

### Core Application Structure
This is an MCP (Model Control Protocol) chat application that enables interactive AI conversations with document retrieval and command capabilities.

**Main Components:**
- `main.py`: Entry point, orchestrates MCP clients and starts CLI
- `core/cli_chat.py`: Chat implementation with document and command processing
- `core/cli.py`: CLI interface with auto-completion and command suggestions
- `mcp_client.py`: MCP client wrapper (contains TODO placeholders for full implementation)
- `mcp_server.py`: Complete MCP server with document storage and full feature implementation

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

### Implementation Status

**mcp_server.py:** ✅ Fully implemented with all features:
- Document CRUD operations (read, edit)
- Resource endpoints for document listing and retrieval
- Tool interfaces for all document operations
- Prompt templates for markdown conversion and summarization
- Clean, non-duplicated code using multiple decorators per function

**mcp_client.py:** ⚠️ Contains placeholder implementations:
- All MCP protocol methods are stubbed (list_tools, call_tool, list_prompts, get_prompt, read_resource)
- Needs implementation for full MCP client functionality

### Available MCP Server Features

The server provides these interfaces (using dual decorators for tool + resource/prompt access):

**Document Operations:**
- `read_doc_contents` / `get_document_content`: Read document by ID
- `edit_document`: Edit documents via string replacement
- `list_documents` + `docs://documents` resource: Get all document IDs
- `docs://documents/{doc_id}` resource: Get specific document content

**AI Processing:**
- `rewrite_doc_markdown` + `rewrite_markdown` prompt: Convert to markdown
- `summarize_doc` + `summarize` prompt: Generate document summaries

### Development Notes

- No linting or type checking currently implemented
- Python 3.10+ required
- Uses FastMCP for server implementation
- Uses prompt-toolkit for rich CLI experience
- Async/await throughout for concurrent MCP connections
- Server functions use multiple decorators to avoid code duplication
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

**Important:** Uses `load_dotenv(override=True)` to ensure .env file takes precedence over system environment variables. API key is passed explicitly to Claude service for reliable authentication.

## Architecture Overview

### Core Application Structure
This is an MCP (Model Control Protocol) chat application that enables interactive AI conversations with document retrieval and command capabilities.

**Main Components:**
- `main.py`: Entry point, orchestrates MCP clients and starts CLI
- `core/cli_chat.py`: Chat implementation with document and command processing
- `core/cli.py`: CLI interface with auto-completion and command suggestions
- `mcp_client.py`: Fully implemented MCP client with all protocol methods
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

**✅ COMPLETE - All Core Components Fully Implemented:**

**mcp_server.py:** ✅ Fully implemented with all features:
- Document CRUD operations (read, edit)
- Resource endpoints for document listing and retrieval
- Tool interfaces for all document operations
- Prompt templates for markdown conversion and summarization
- Clean, non-duplicated code using multiple decorators per function

**mcp_client.py:** ✅ Fully implemented MCP client:
- All MCP protocol methods implemented (list_tools, call_tool, list_prompts, get_prompt, read_resource)
- Proper session management and error handling
- Resource response parsing and content extraction
- Complete client-server communication functionality

**core/claude.py:** ✅ Enhanced authentication:
- Accepts explicit API key parameter for reliable authentication
- Fallback to environment variable if no key provided
- Eliminates environment variable conflicts

**main.py:** ✅ Robust configuration loading:
- Uses `load_dotenv(override=True)` for reliable .env file precedence
- Explicit API key passing to eliminate authentication issues
- Complete application orchestration

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
- Explicit API key management prevents authentication conflicts
- Resource parsing handles MCP response objects properly

### Production Readiness

**✅ Ready for Production Use:**
- All core functionality implemented and tested
- Reliable API key loading from .env files
- Complete MCP client-server communication
- Document retrieval and processing working
- Interactive CLI with auto-completion
- Error handling and session management
- No remaining TODO items in critical paths
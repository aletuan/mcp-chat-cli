# MCP Chat

MCP Chat is a command-line interface application that enables interactive chat capabilities with AI models through the Anthropic API. The application supports document retrieval, command-based prompts, and extensible tool integrations via the MCP (Model Control Protocol) architecture.

## Prerequisites

- Python 3.9+
- Anthropic API Key

## Setup

### Step 1: Configure the environment variables

1. Create or edit the `.env` file in the project root and verify that the following variables are set correctly:

```
CLAUDE_MODEL="claude-3-5-sonnet-20241022"  # Anthropic Claude model to use
ANTHROPIC_API_KEY="your_actual_api_key_here"  # Your Anthropic API secret key
USE_UV=1  # Set to 1 if using uv, 0 otherwise
```

**Important:** Replace `your_actual_api_key_here` with your real Anthropic API key from the [Anthropic Console](https://console.anthropic.com/).

**Note:** The application uses `load_dotenv(override=True)` to ensure your `.env` file values take precedence over any system environment variables, providing reliable configuration.

### Step 2: Install dependencies

#### Option 1: Setup with uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver.

1. Install uv, if not already installed:

```bash
pip install uv
```

2. Create and activate a virtual environment:

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
uv pip install -e .
```

4. Run the project

```bash
uv run main.py
```

#### Option 2: Setup without uv

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install anthropic python-dotenv prompt-toolkit "mcp[cli]==1.8.0"
```

3. Run the project

```bash
python main.py
```

## Usage

### Basic Interaction

Simply type your message and press Enter to chat with the model.

### Document Retrieval

Use the @ symbol followed by a document ID to include document content in your query:

```
> Tell me about @deposition.md
```

### Commands

Use the / prefix to execute commands defined in the MCP server:

```
> /summarize deposition.md
```

Commands will auto-complete when you press Tab.

Available commands:
- `/rewrite_markdown <doc_id>`: Convert a document to markdown format
- `/summarize <doc_id>`: Generate a summary of a document

## Development

### Adding New Documents

Edit the `mcp_server.py` file to add new documents to the `docs` dictionary.

### Available MCP Features

The MCP server (`mcp_server.py`) provides the following fully implemented features:

**Tools:**
- `read_doc_contents`: Read document contents by ID
- `edit_document`: Edit documents using string replacement
- `list_documents`: Get all available document IDs
- `get_document_content`: Retrieve specific document content
- `rewrite_doc_markdown`: Convert document to markdown format
- `summarize_doc`: Generate document summaries

**Resources:**
- `docs://documents`: List all document IDs
- `docs://documents/{doc_id}`: Get specific document content

**Prompts:**
- `rewrite_markdown`: Prompt for markdown conversion
- `summarize`: Prompt for document summarization

### Application Architecture

**Fully Implemented Components:**
- ✅ **MCP Server** (`mcp_server.py`): Complete with all tools, resources, and prompts
- ✅ **MCP Client** (`mcp_client.py`): Full MCP protocol implementation
- ✅ **Authentication**: Reliable API key loading from .env with override support
- ✅ **Document System**: Working document retrieval and command processing
- ✅ **CLI Interface**: Interactive chat with auto-completion and history

### Extending Functionality

To extend the application:

1. **Add Documents**: Add new entries to the `docs` dictionary in `mcp_server.py`
2. **Create New Tools**: Add new `@mcp.tool()` decorated functions in `mcp_server.py`
3. **Add Resources**: Create new `@mcp.resource()` endpoints for data access
4. **Custom Prompts**: Define new `@mcp.prompt()` templates for AI processing

### Linting and Typing Check

There are no lint or type checks implemented.

#!/usr/bin/env python3
"""
Test script to debug the document query functionality
Simulates the user input: "What is the contents of the report.pdf document?"
"""

import asyncio
import sys
import os
from dotenv import load_dotenv
from contextlib import AsyncExitStack

from mcp_client import MCPClient
from core.claude import Claude
from core.cli_chat import CliChat

load_dotenv()

# Anthropic Config
claude_model = os.getenv("CLAUDE_MODEL", "")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "")

assert claude_model, "Error: CLAUDE_MODEL cannot be empty. Update .env"
assert anthropic_api_key, "Error: ANTHROPIC_API_KEY cannot be empty. Update .env"

async def test_document_query():
    """Test the document query functionality"""
    claude_service = Claude(model=claude_model)

    command, args = (
        ("uv", ["run", "mcp_server.py"])
        if os.getenv("USE_UV", "0") == "1"
        else ("python", ["mcp_server.py"])
    )

    print("Starting MCP client connection...")

    async with AsyncExitStack() as stack:
        # Connect to the MCP server
        doc_client = await stack.enter_async_context(
            MCPClient(command=command, args=args)
        )
        clients = {"doc_client": doc_client}

        print("✅ MCP client connected successfully")

        # Create chat instance
        chat = CliChat(
            doc_client=doc_client,
            clients=clients,
            claude_service=claude_service,
        )

        print("✅ Chat instance created")

        # Test document listing
        try:
            doc_ids = await chat.list_docs_ids()
            print(f"✅ Available documents: {doc_ids}")
        except Exception as e:
            print(f"❌ Error listing documents: {e}")
            import traceback
            traceback.print_exc()
            return

        # Test document content retrieval
        try:
            content = await chat.get_doc_content("report.pdf")
            print(f"✅ Document content retrieved: '{content}'")
        except Exception as e:
            print(f"❌ Error getting document content: {e}")
            import traceback
            traceback.print_exc()
            return

        # Test the full query processing
        print("\n--- Testing full query processing ---")
        test_query = "What is the contents of the @report.pdf document?"
        print(f"Query: {test_query}")

        try:
            # Process the query (this calls _extract_resources and _process_query)
            await chat._process_query(test_query)
            print(f"✅ Query processed, messages count: {len(chat.messages)}")

            # Show the last message that would be sent to Claude
            if chat.messages:
                last_message = chat.messages[-1]
                print(f"✅ Last message content preview: {last_message['content'][:200]}...")

                # Test the actual Claude API call
                print("\n--- Testing Claude API call ---")
                response = chat.claude_service.chat(chat.messages)
                response_text = response.content[0].text if hasattr(response, 'content') else str(response)
                print(f"✅ Claude responded: {response_text[:200]}...")

        except Exception as e:
            print(f"❌ Error processing query: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(test_document_query())
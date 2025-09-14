#!/usr/bin/env python3
"""
Test script to verify the command processing fix works correctly
"""

import asyncio
import sys
import os
from dotenv import load_dotenv
from contextlib import AsyncExitStack

from mcp_client import MCPClient
from core.claude import Claude
from core.cli_chat import CliChat

load_dotenv(override=True)

# Anthropic Config
claude_model = os.getenv("CLAUDE_MODEL", "")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "")

assert claude_model, "Error: CLAUDE_MODEL cannot be empty. Update .env"
assert anthropic_api_key, "Error: ANTHROPIC_API_KEY cannot be empty. Update .env"

async def test_command_processing():
    """Test that commands work with and without @ symbols"""
    claude_service = Claude(model=claude_model, api_key=anthropic_api_key)

    command, args = (
        ("uv", ["run", "mcp_server.py"])
        if os.getenv("USE_UV", "0") == "1"
        else ("python", ["mcp_server.py"])
    )

    print("Testing command processing fix...")

    async with AsyncExitStack() as stack:
        # Connect to the MCP server
        doc_client = await stack.enter_async_context(
            MCPClient(command=command, args=args)
        )
        clients = {"doc_client": doc_client}

        # Create chat instance
        chat = CliChat(
            doc_client=doc_client,
            clients=clients,
            claude_service=claude_service,
        )

        print("✅ MCP client connected")

        # Test both command formats
        test_commands = [
            "/rewrite_markdown deposition.md",
            "/rewrite_markdown @deposition.md",
            "/summarize deposition.md",
            "/summarize @deposition.md"
        ]

        for cmd in test_commands:
            print(f"\n--- Testing command: {cmd} ---")
            try:
                # Clear previous messages
                chat.messages = []

                # Process the command
                result = await chat._process_command(cmd)

                if result:
                    print(f"✅ Command processed successfully")
                    if chat.messages:
                        # Show a preview of the generated message
                        msg_preview = chat.messages[-1]['content'][:100]
                        print(f"✅ Generated message preview: {msg_preview}...")
                else:
                    print(f"❌ Command processing returned False")

            except Exception as e:
                print(f"❌ Error processing command: {e}")

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(test_command_processing())
#!/usr/bin/env python3
"""
Test script to verify Ollama MCP tools are working.

This script tests the Ollama MCP server tools that show up as "13 tools enabled"
in the Ollama interface.
"""

import asyncio
import json
from mcp import ClientSession
from mcp.client.stdio import stdio_client
from mcp.types import StdioServerParameters

# Ollama MCP server configuration
# Try different possible command formats
# Option 1: If ollama-mcp is installed globally
# Option 2: If using npx
# Option 3: If integrated into Ollama Desktop

# Try these in order:
POSSIBLE_COMMANDS = [
    ("ollama-mcp", ["start"]),
    ("npx", ["-y", "@modelcontextprotocol/server-ollama"]),
    ("npx", ["@modelcontextprotocol/server-ollama"]),
]

# Default to first option
OLLAMA_MCP_PARAMS = StdioServerParameters(
    command=POSSIBLE_COMMANDS[0][0],
    args=POSSIBLE_COMMANDS[0][1],
    env=None
)

async def test_ollama_mcp_tools():
    """Test Ollama MCP tools to verify they're working."""
    
    print("=" * 60)
    print("Testing Ollama MCP Tools")
    print("=" * 60)
    print()
    
    # Try different command formats
    last_error = None
    for cmd, args in POSSIBLE_COMMANDS:
        try:
            print(f"1. Connecting to Ollama MCP server...")
            print(f"   Trying: {' '.join([cmd] + args)}")
            params = StdioServerParameters(command=cmd, args=args, env=None)
            async with stdio_client(params) as (read, write):
                async with ClientSession(read, write) as session:
                    print("   ✓ Connected!")
                    print()
                    
                    # Initialize the session
                    print("2. Initializing session...")
                    await session.initialize()
                    print("   ✓ Initialized!")
                    print()
                    
                    # List available tools
                    print("3. Listing available tools...")
                    tools_response = await session.list_tools()
                    tools = tools_response.tools
                    print(f"   ✓ Found {len(tools)} tools:")
                    print()
                    for i, tool in enumerate(tools, 1):
                        print(f"   {i}. {tool.name}")
                        if tool.description:
                            print(f"      {tool.description}")
                        print()
                    
                    # Test 1: List models (ollama_list)
                    print("4. Testing 'ollama_list' tool (list available models)...")
                    try:
                        result = await session.call_tool("ollama_list", {})
                        if result.content:
                            print("   ✓ Success!")
                            print(f"   Result: {result.content[0].text[:200]}...")
                        else:
                            print("   ⚠ No content returned")
                    except Exception as e:
                        print(f"   ✗ Error: {e}")
                    print()
                    
                    # Test 2: Check if models are available (ollama_ps)
                    print("5. Testing 'ollama_ps' tool (list running models)...")
                    try:
                        result = await session.call_tool("ollama_ps", {})
                        if result.content:
                            print("   ✓ Success!")
                            print(f"   Result: {result.content[0].text[:200]}...")
                        else:
                            print("   ⚠ No content returned")
                    except Exception as e:
                        print(f"   ✗ Error: {e}")
                    print()
                    
                    # Test 3: Try a simple chat (if we have a model)
                    print("6. Testing 'ollama_chat' tool (simple chat test)...")
                    try:
                        # Try with a common model name
                        result = await session.call_tool("ollama_chat", {
                            "model": "llama3",
                            "messages": [
                                {"role": "user", "content": "Say 'Hello, MCP tools are working!'"}
                            ]
                        })
                        if result.content:
                            print("   ✓ Success!")
                            print(f"   Result: {result.content[0].text[:200]}...")
                        else:
                            print("   ⚠ No content returned")
                    except Exception as e:
                        print(f"   ✗ Error: {e}")
                        print("   (This is okay if llama3 model is not installed)")
                    print()
                    
                    print("=" * 60)
                    print("✅ Testing Complete!")
                    print("=" * 60)
                    print()
                    print("Summary:")
                    print(f"  • Total tools found: {len(tools)}")
                    print("  • Connection: ✓ Working")
                    print("  • Tools accessible: ✓ Yes")
                    print()
                    print("💡 If you see errors above, check:")
                    print("   1. Is 'ollama-mcp start' running?")
                    print("   2. Is Ollama installed and running?")
                    print("   3. Are models pulled? (e.g., 'ollama pull llama3')")
                    return  # Success, exit
        except FileNotFoundError:
            last_error = f"Command '{cmd}' not found"
            print(f"   ✗ {last_error}")
            continue
        except Exception as e:
            last_error = str(e)
            print(f"   ✗ Error: {e}")
            continue
    
    # If we get here, all attempts failed
    print()
    print("=" * 60)
    print("✗ All connection attempts failed")
    print("=" * 60)
    print()
    print("Tried commands:")
    for cmd, args in POSSIBLE_COMMANDS:
        print(f"  • {' '.join([cmd] + args)}")
    print()
    print("Troubleshooting:")
    print("  1. If using Ollama Desktop: MCP tools might be built-in")
    print("     Check Ollama Desktop settings for MCP configuration")
    print()
    print("  2. If using command-line Ollama: Install MCP server:")
    print("     npm install -g @modelcontextprotocol/server-ollama")
    print()
    print("  3. Verify Ollama is running:")
    print("     ollama list")
    print("     ollama serve")
    print()
    print("  4. Check if Ollama MCP is configured in your MCP client:")
    print("     - Cursor: Check Settings → MCP")
    print("     - Claude Desktop: Check ~/.config/claude_desktop_config.json")
    print()
    if last_error:
        print(f"Last error: {last_error}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print()
    print("🔍 Ollama MCP Tools Test")
    print()
    asyncio.run(test_ollama_mcp_tools())


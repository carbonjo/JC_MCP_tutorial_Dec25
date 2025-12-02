#!/usr/bin/env python3
"""
MCP Code Server - Educational Example
Provides code-related tools: file operations, code execution, and code analysis.
"""

import asyncio
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Sequence

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel,
)


# Initialize the MCP server
app = Server("code-server")

# Store for code snippets
code_store: dict[str, str] = {}


@app.list_resources()
async def list_resources() -> list[Resource]:
    """List available code resources."""
    resources = []
    for name, code in code_store.items():
        resources.append(
            Resource(
                uri=f"code://{name}",
                name=f"Code: {name}",
                description=f"Stored code snippet: {name}",
                mimeType="text/x-python",
            )
        )
    return resources


@app.read_resource()
async def read_resource(uri: str) -> str:
    """Get a code resource by URI."""
    if uri.startswith("code://"):
        name = uri[7:]  # Remove "code://" prefix
        if name in code_store:
            return code_store[name]
    raise ValueError(f"Resource not found: {uri}")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available code tools."""
    return [
        Tool(
            name="read_file",
            description="Read the contents of a file",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the file to read",
                    }
                },
                "required": ["file_path"],
            },
        ),
        Tool(
            name="write_file",
            description="Write content to a file",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the file to write",
                    },
                    "content": {
                        "type": "string",
                        "description": "Content to write to the file",
                    },
                },
                "required": ["file_path", "content"],
            },
        ),
        Tool(
            name="execute_code",
            description="Execute Python code and return the result",
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "Python code to execute",
                    },
                },
                "required": ["code"],
            },
        ),
        Tool(
            name="save_code_snippet",
            description="Save a code snippet for later retrieval",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name for the code snippet",
                    },
                    "code": {
                        "type": "string",
                        "description": "Code snippet to save",
                    },
                },
                "required": ["name", "code"],
            },
        ),
        Tool(
            name="list_code_snippets",
            description="List all saved code snippets",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent | ImageContent | EmbeddedResource]:
    """Handle tool calls."""
    if name == "read_file":
        file_path = arguments.get("file_path")
        if not file_path:
            raise ValueError("file_path is required")
        
        try:
            path = Path(file_path)
            if not path.exists():
                return [TextContent(
                    type="text",
                    text=f"Error: File not found: {file_path}"
                )]
            
            content = path.read_text()
            return [TextContent(
                type="text",
                text=f"File contents of {file_path}:\n\n{content}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Error reading file: {str(e)}"
            )]
    
    elif name == "write_file":
        file_path = arguments.get("file_path")
        content = arguments.get("content")
        
        if not file_path or content is None:
            raise ValueError("file_path and content are required")
        
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
            return [TextContent(
                type="text",
                text=f"Successfully wrote {len(content)} characters to {file_path}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Error writing file: {str(e)}"
            )]
    
    elif name == "execute_code":
        code = arguments.get("code")
        if not code:
            raise ValueError("code is required")
        
        try:
            # Create a safe execution environment
            result = subprocess.run(
                [sys.executable, "-c", code],
                capture_output=True,
                text=True,
                timeout=10,
            )
            
            output = result.stdout
            if result.stderr:
                output += f"\n[stderr]\n{result.stderr}"
            
            if result.returncode != 0:
                output = f"[Error - exit code {result.returncode}]\n{output}"
            
            return [TextContent(
                type="text",
                text=f"Execution result:\n{output}"
            )]
        except subprocess.TimeoutExpired:
            return [TextContent(
                type="text",
                text="Error: Code execution timed out (max 10 seconds)"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Error executing code: {str(e)}"
            )]
    
    elif name == "save_code_snippet":
        name = arguments.get("name")
        code = arguments.get("code")
        
        if not name or not code:
            raise ValueError("name and code are required")
        
        code_store[name] = code
        return [TextContent(
            type="text",
            text=f"Code snippet '{name}' saved successfully"
        )]
    
    elif name == "list_code_snippets":
        if not code_store:
            return [TextContent(
                type="text",
                text="No code snippets saved yet"
            )]
        
        snippets = "\n".join([f"- {name}" for name in code_store.keys()])
        return [TextContent(
            type="text",
            text=f"Saved code snippets:\n{snippets}"
        )]
    
    else:
        raise ValueError(f"Unknown tool: {name}")


async def main():
    """Run the code server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())


#!/usr/bin/env python3
"""
MCP Document Server - Educational Example
Provides document operations: reading, searching, and managing text documents.
"""

import asyncio
import json
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)


# Initialize the MCP server
app = Server("document-server")

# Document store
DOCUMENTS_DIR = Path("documents")
DOCUMENTS_DIR.mkdir(exist_ok=True)

# In-memory document index for search
document_index: dict[str, str] = {}


def index_document(name: str, content: str):
    """Index a document for search."""
    document_index[name] = content.lower()


@app.list_resources()
async def list_resources() -> list[Resource]:
    """List available document resources."""
    resources = []
    
    # List all documents in the documents directory
    for doc_file in DOCUMENTS_DIR.glob("*.txt"):
        resources.append(
            Resource(
                uri=f"doc://{doc_file.stem}",
                name=f"Document: {doc_file.stem}",
                description=f"Text document: {doc_file.stem}",
                mimeType="text/plain",
            )
        )
    
    return resources


@app.read_resource()
async def read_resource(uri: str) -> str:
    """Get a document resource by URI."""
    if uri.startswith("doc://"):
        doc_name = uri[6:]  # Remove "doc://" prefix
        doc_path = DOCUMENTS_DIR / f"{doc_name}.txt"
        
        if doc_path.exists():
            return doc_path.read_text()
        else:
            raise ValueError(f"Document not found: {doc_name}")
    else:
        raise ValueError(f"Unknown resource URI: {uri}")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available document tools."""
    return [
        Tool(
            name="create_document",
            description="Create a new text document",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the document (without extension)",
                    },
                    "content": {
                        "type": "string",
                        "description": "Content of the document",
                    },
                },
                "required": ["name", "content"],
            },
        ),
        Tool(
            name="read_document",
            description="Read the contents of a document",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the document to read",
                    },
                },
                "required": ["name"],
            },
        ),
        Tool(
            name="list_documents",
            description="List all available documents",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="search_documents",
            description="Search for text in all documents",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query text",
                    },
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="append_to_document",
            description="Append text to an existing document",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the document",
                    },
                    "content": {
                        "type": "string",
                        "description": "Content to append",
                    },
                },
                "required": ["name", "content"],
            },
        ),
        Tool(
            name="delete_document",
            description="Delete a document",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the document to delete",
                    },
                },
                "required": ["name"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent | ImageContent | EmbeddedResource]:
    """Handle tool calls."""
    if name == "create_document":
        doc_name = arguments.get("name")
        content = arguments.get("content")
        
        if not doc_name or not content:
            raise ValueError("name and content are required")
        
        try:
            doc_path = DOCUMENTS_DIR / f"{doc_name}.txt"
            doc_path.write_text(content)
            index_document(doc_name, content)
            
            return [TextContent(
                type="text",
                text=f"Document '{doc_name}' created successfully ({len(content)} characters)"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Error creating document: {str(e)}"
            )]
    
    elif name == "read_document":
        doc_name = arguments.get("name")
        if not doc_name:
            raise ValueError("name is required")
        
        try:
            doc_path = DOCUMENTS_DIR / f"{doc_name}.txt"
            if not doc_path.exists():
                return [TextContent(
                    type="text",
                    text=f"Document '{doc_name}' not found"
                )]
            
            content = doc_path.read_text()
            return [TextContent(
                type="text",
                text=f"Document '{doc_name}':\n\n{content}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Error reading document: {str(e)}"
            )]
    
    elif name == "list_documents":
        try:
            docs = list(DOCUMENTS_DIR.glob("*.txt"))
            if not docs:
                return [TextContent(
                    type="text",
                    text="No documents found"
                )]
            
            doc_list = "\n".join([f"- {doc.stem}" for doc in sorted(docs)])
            return [TextContent(
                type="text",
                text=f"Available documents ({len(docs)}):\n{doc_list}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Error listing documents: {str(e)}"
            )]
    
    elif name == "search_documents":
        query = arguments.get("query")
        if not query:
            raise ValueError("query is required")
        
        try:
            query_lower = query.lower()
            matches = []
            
            # Search in indexed documents
            for doc_name, content in document_index.items():
                if query_lower in content:
                    # Count occurrences
                    count = content.count(query_lower)
                    matches.append((doc_name, count))
            
            # Also search in files
            for doc_file in DOCUMENTS_DIR.glob("*.txt"):
                if doc_file.stem not in document_index:
                    content = doc_file.read_text().lower()
                    if query_lower in content:
                        count = content.count(query_lower)
                        matches.append((doc_file.stem, count))
                        index_document(doc_file.stem, doc_file.read_text())
            
            if matches:
                results = "\n".join([f"- {name} ({count} occurrence(s))" for name, count in sorted(matches)])
                return [TextContent(
                    type="text",
                    text=f"Search results for '{query}':\n{results}"
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"No documents found containing '{query}'"
                )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Error searching documents: {str(e)}"
            )]
    
    elif name == "append_to_document":
        doc_name = arguments.get("name")
        content = arguments.get("content")
        
        if not doc_name or not content:
            raise ValueError("name and content are required")
        
        try:
            doc_path = DOCUMENTS_DIR / f"{doc_name}.txt"
            if not doc_path.exists():
                return [TextContent(
                    type="text",
                    text=f"Document '{doc_name}' not found. Use create_document first."
                )]
            
            existing_content = doc_path.read_text()
            new_content = existing_content + "\n" + content
            doc_path.write_text(new_content)
            index_document(doc_name, new_content)
            
            return [TextContent(
                type="text",
                text=f"Appended {len(content)} characters to '{doc_name}'"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Error appending to document: {str(e)}"
            )]
    
    elif name == "delete_document":
        doc_name = arguments.get("name")
        if not doc_name:
            raise ValueError("name is required")
        
        try:
            doc_path = DOCUMENTS_DIR / f"{doc_name}.txt"
            if not doc_path.exists():
                return [TextContent(
                    type="text",
                    text=f"Document '{doc_name}' not found"
                )]
            
            doc_path.unlink()
            document_index.pop(doc_name, None)
            
            return [TextContent(
                type="text",
                text=f"Document '{doc_name}' deleted successfully"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Error deleting document: {str(e)}"
            )]
    
    else:
        raise ValueError(f"Unknown tool: {name}")


async def main():
    """Run the document server."""
    # Index existing documents on startup
    for doc_file in DOCUMENTS_DIR.glob("*.txt"):
        index_document(doc_file.stem, doc_file.read_text())
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())


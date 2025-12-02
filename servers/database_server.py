#!/usr/bin/env python3
"""
MCP Database Server - Educational Example
Provides database operations using SQLite.
"""

import asyncio
import json
import sqlite3
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
app = Server("database-server")

# Default database path
DB_PATH = Path("example.db")


def get_connection():
    """Get a database connection."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn


def init_database():
    """Initialize the database with example tables."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create example tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            age INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            category TEXT,
            stock INTEGER DEFAULT 0
        )
    """)
    
    # Insert sample data if tables are empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO users (name, email, age) VALUES (?, ?, ?)
        """, [
            ("Alice Johnson", "alice@example.com", 30),
            ("Bob Smith", "bob@example.com", 25),
            ("Charlie Brown", "charlie@example.com", 35),
        ])
    
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO products (name, price, category, stock) VALUES (?, ?, ?, ?)
        """, [
            ("Laptop", 999.99, "Electronics", 10),
            ("Mouse", 29.99, "Electronics", 50),
            ("Desk Chair", 199.99, "Furniture", 15),
        ])
    
    conn.commit()
    conn.close()


@app.list_resources()
async def list_resources() -> list[Resource]:
    """List available database resources."""
    return [
        Resource(
            uri="db://schema",
            name="Database Schema",
            description="Schema information for the database",
            mimeType="application/json",
        ),
        Resource(
            uri="db://tables",
            name="Database Tables",
            description="List of all tables in the database",
            mimeType="application/json",
        ),
    ]


@app.read_resource()
async def read_resource(uri: str) -> str:
    """Get a database resource by URI."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        if uri == "db://schema":
            cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table'")
            tables = {}
            for row in cursor.fetchall():
                tables[row[0]] = row[1]
            return json.dumps(tables, indent=2)
        
        elif uri == "db://tables":
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            return json.dumps(tables, indent=2)
        
        else:
            raise ValueError(f"Unknown resource: {uri}")
    finally:
        conn.close()


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available database tools."""
    return [
        Tool(
            name="execute_query",
            description="Execute a SQL query and return results",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "SQL query to execute (SELECT, INSERT, UPDATE, DELETE)",
                    },
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="list_tables",
            description="List all tables in the database",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="describe_table",
            description="Get schema information for a specific table",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "Name of the table to describe",
                    },
                },
                "required": ["table_name"],
            },
        ),
        Tool(
            name="insert_user",
            description="Insert a new user into the users table",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "User's name",
                    },
                    "email": {
                        "type": "string",
                        "description": "User's email",
                    },
                    "age": {
                        "type": "integer",
                        "description": "User's age",
                    },
                },
                "required": ["name", "email", "age"],
            },
        ),
        Tool(
            name="get_user",
            description="Get a user by email",
            inputSchema={
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "User's email",
                    },
                },
                "required": ["email"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent | ImageContent | EmbeddedResource]:
    """Handle tool calls."""
    if name == "execute_query":
        query = arguments.get("query")
        if not query:
            raise ValueError("query is required")
        
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            # Only allow SELECT, INSERT, UPDATE, DELETE for safety
            query_upper = query.strip().upper()
            if not any(query_upper.startswith(cmd) for cmd in ["SELECT", "INSERT", "UPDATE", "DELETE"]):
                return [TextContent(
                    type="text",
                    text="Error: Only SELECT, INSERT, UPDATE, DELETE queries are allowed"
                )]
            
            cursor.execute(query)
            
            if query_upper.startswith("SELECT"):
                rows = cursor.fetchall()
                if rows:
                    # Convert rows to list of dicts
                    results = [dict(row) for row in rows]
                    return [TextContent(
                        type="text",
                        text=f"Query results ({len(results)} rows):\n{json.dumps(results, indent=2)}"
                    )]
                else:
                    return [TextContent(
                        type="text",
                        text="Query executed successfully, but returned no results"
                    )]
            else:
                conn.commit()
                return [TextContent(
                    type="text",
                    text=f"Query executed successfully. Rows affected: {cursor.rowcount}"
                )]
        except Exception as e:
            conn.rollback()
            return [TextContent(
                type="text",
                text=f"Error executing query: {str(e)}"
            )]
        finally:
            conn.close()
    
    elif name == "list_tables":
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            return [TextContent(
                type="text",
                text=f"Database tables:\n" + "\n".join([f"- {table}" for table in tables])
            )]
        finally:
            conn.close()
    
    elif name == "describe_table":
        table_name = arguments.get("table_name")
        if not table_name:
            raise ValueError("table_name is required")
        
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            if not columns:
                return [TextContent(
                    type="text",
                    text=f"Table '{table_name}' not found"
                )]
            
            column_info = []
            for col in columns:
                column_info.append(f"- {col[1]} ({col[2]})" + (f" NOT NULL" if col[3] else ""))
            
            return [TextContent(
                type="text",
                text=f"Table '{table_name}' schema:\n" + "\n".join(column_info)
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Error describing table: {str(e)}"
            )]
        finally:
            conn.close()
    
    elif name == "insert_user":
        name = arguments.get("name")
        email = arguments.get("email")
        age = arguments.get("age")
        
        if not all([name, email, age is not None]):
            raise ValueError("name, email, and age are required")
        
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
                (name, email, age)
            )
            conn.commit()
            return [TextContent(
                type="text",
                text=f"User '{name}' inserted successfully with ID {cursor.lastrowid}"
            )]
        except sqlite3.IntegrityError as e:
            return [TextContent(
                type="text",
                text=f"Error: {str(e)}"
            )]
        except Exception as e:
            conn.rollback()
            return [TextContent(
                type="text",
                text=f"Error inserting user: {str(e)}"
            )]
        finally:
            conn.close()
    
    elif name == "get_user":
        email = arguments.get("email")
        if not email:
            raise ValueError("email is required")
        
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            row = cursor.fetchone()
            
            if row:
                user_dict = dict(row)
                return [TextContent(
                    type="text",
                    text=f"User found:\n{json.dumps(user_dict, indent=2)}"
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"No user found with email: {email}"
                )]
        finally:
            conn.close()
    
    else:
        raise ValueError(f"Unknown tool: {name}")


async def main():
    """Run the database server."""
    # Initialize database on startup
    init_database()
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())


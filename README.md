# MCP Agents Educational Project

This is an educational, minimal project that demonstrates the Model Context Protocol (MCP) with three different types of servers:

1. **Code Server** - File operations and code execution
2. **Database Server** - SQLite database operations
3. **Document Server** - Document management and search

## What is MCP?

The Model Context Protocol (MCP) is a standardized protocol that allows AI agents to interact with various services and tools. It provides a common interface for:
- **Tools**: Functions that agents can call to perform actions
- **Resources**: Data that agents can access
- **Prompts**: Reusable prompt templates

## Project Structure

```
.
├── servers/
│   ├── code_server.py          # Code server implementation
│   ├── database_server.py      # Database server implementation
│   └── document_server.py      # Document server implementation
├── notebooks/
│   ├── mcp_client_demo.ipynb   # Jupyter notebook with basic MCP demos
│   └── mcp_llm_agent.ipynb     # Jupyter notebook with LLM integration
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Make server scripts executable (optional):**
   ```bash
   chmod +x servers/*.py
   ```

## Running the Demo

1. **Start Jupyter Notebook:**
   ```bash
   jupyter notebook
   ```

2. **Open the demo notebooks (IN ORDER):**
   - **START HERE**: `notebooks/mcp_client_demo.ipynb` - Basic MCP demo
     - Run cells **one at a time**
     - Wait for each cell to complete before running the next
   - **THEN TRY**: `notebooks/mcp_llm_agent.ipynb` - Advanced LLM integration
     - Requires understanding of the basic demo first

3. **Important Notes:**
   - **Run cells sequentially**: Don't run all cells at once
   - **Wait for completion**: Look for `[1]`, `[2]`, `[3]` (cell numbers)
   - **`[*]` means running**: Wait for it to finish
   - **`await` works in Jupyter**: No need for `asyncio.run()`
   - **Servers start automatically**: No need to manually start them

4. **Troubleshooting:**
   - If execution numbers don't show: See `NOTEBOOK_TROUBLESHOOTING.md`
   - If cells hang: Press `Ctrl+C` (or `Cmd+C`) to interrupt, then restart kernel
   - If connection errors: See `GETTING_STARTED.md` for detailed help

## LLM Integration

The project includes LLM integration to create intelligent agents that can understand natural language and use MCP tools. Two methods are supported:

### Method 1: Ollama (Local Models)

Run LLMs locally without API keys:

1. **Install Ollama**: Download from [https://ollama.ai](https://ollama.ai)
2. **Pull a model**: `ollama pull llama3` (or any other model)
3. **Start Ollama service**: `ollama serve`
4. **Use in notebook**: The `mcp_llm_agent.ipynb` notebook will automatically detect and use Ollama

### Method 2: API-based Models (OpenAI & Gemini)

Use cloud-based LLM APIs:

1. **Get API Keys**:
   - **OpenAI**: Get from [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
   - **Gemini**: Get from [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

2. **Set API Keys** (use .env file):
   - **Create `.env` file** in the project root:
     ```bash
     cp .env.example .env
     ```
   - **Edit `.env` file** and add your keys:
     ```
     OPENAI_API_KEY=your-openai-key-here
     GEMINI_API_KEY=your-gemini-key-here
     ```
   - **Note**: You only need to set the keys for providers you want to use
   - The `.env` file is gitignored for security

3. **Use in notebook**: Open `mcp_llm_agent.ipynb` - keys will be loaded automatically from `.env`

### Example LLM Agent Usage

```python
# Using Ollama (local)
result = await intelligent_agent(
    "List all users in the database",
    provider="ollama",
    model="llama3"
)

# Using OpenAI
result = await intelligent_agent(
    "Create a document with database statistics",
    provider="openai",
    model="gpt-4o-mini"
)

# Using Gemini
result = await intelligent_agent(
    "Write a Python function to calculate factorial",
    provider="gemini"
)
```

## Server Details

### Code Server (`code_server.py`)

Provides tools for:
- `read_file`: Read file contents
- `write_file`: Write content to files
- `execute_code`: Execute Python code
- `save_code_snippet`: Save code snippets for later use
- `list_code_snippets`: List all saved code snippets

**Resources:**
- Code snippets stored in memory (accessible via `code://` URIs)

### Database Server (`database_server.py`)

Provides tools for:
- `execute_query`: Execute SQL queries (SELECT, INSERT, UPDATE, DELETE)
- `list_tables`: List all database tables
- `describe_table`: Get schema information for a table
- `insert_user`: Insert a new user (convenience method)
- `get_user`: Get a user by email (convenience method)

**Resources:**
- Database schema (`db://schema`)
- List of tables (`db://tables`)

**Note:** The server automatically creates an SQLite database (`example.db`) with sample data on first run.

### Document Server (`document_server.py`)

Provides tools for:
- `create_document`: Create a new text document
- `read_document`: Read document contents
- `list_documents`: List all available documents
- `search_documents`: Search for text across all documents
- `append_to_document`: Append text to an existing document
- `delete_document`: Delete a document

**Resources:**
- Documents stored in `documents/` directory (accessible via `doc://` URIs)

## How MCP Works

### Transport Mechanisms

MCP supports multiple transport mechanisms:

1. **stdio (Standard Input/Output)** - Used in this project
   - ✅ Simple: No network configuration needed
   - ✅ Secure: No exposed ports
   - ✅ Process management: Client spawns server
   - ❌ Local only: Cannot connect to remote servers
   - ❌ One client per server: Each client spawns its own process

2. **HTTP/SSE (Server-Sent Events)** - Alternative option
   - ✅ Remote access: Connect to servers on different machines
   - ✅ Scalable: Multiple clients can share one server
   - ✅ Web integration: Can be accessed from browsers
   - ❌ More complex: Requires web server framework
   - ❌ Security: Needs authentication/authorization

**Why stdio in this project?**
- Educational focus: Simpler to understand and set up
- Local development: Perfect for learning and testing
- MCP standard: Primary transport mechanism in MCP spec
- No dependencies: Works out-of-the-box

**When to use HTTP instead:**
- Production deployments
- Remote server access
- Multiple clients sharing one server
- Web browser integration

See `TRANSPORT_COMPARISON.md` for detailed comparison.

### Communication Flow

1. **Server**: An MCP server exposes tools and resources via stdio (or HTTP)
2. **Client**: An MCP client connects to the server and can:
   - List available tools
   - Call tools with arguments
   - List available resources
   - Access resources by URI

3. **Communication**: Uses JSON-RPC over stdio (or HTTP/SSE) for communication

## Example Usage

### Basic MCP Demo (`mcp_client_demo.ipynb`)

The basic notebook demonstrates:
- Connecting to each server
- Listing available tools
- Calling tools with different parameters
- Accessing resources
- Combining multiple servers in a workflow

### LLM Agent Demo (`mcp_llm_agent.ipynb`)

The LLM agent notebook demonstrates:
- Using Ollama for local LLM inference
- Using OpenAI API for cloud-based LLMs
- Using Google Gemini API
- Natural language interaction with MCP servers
- Intelligent tool selection and execution
- Multi-step workflow automation

## Educational Value

This project illustrates:
- How to create MCP servers
- How to implement tools and resources
- How to connect clients to servers
- How to use multiple servers together
- How to integrate LLMs with MCP servers
- How to create intelligent agents that understand natural language
- Real-world patterns for agentic applications

## Transport Options

### Current Implementation: stdio

The servers in this project use **stdio transport**, which is:
- Simple to set up
- Secure (no network ports)
- Perfect for local development
- The standard MCP transport

### Adding HTTP Support

To use HTTP transport instead:

1. **Install HTTP dependencies** (optional):
   ```bash
   pip install fastapi uvicorn
   ```

2. **Run server as HTTP service**:
   ```bash
   python servers/code_server_http.py
   ```

3. **Connect client via HTTP**:
   ```python
   from mcp.client.sse import sse_client
   # Use HTTP client instead of stdio_client
   ```

See `TRANSPORT_COMPARISON.md` for detailed comparison of stdio vs HTTP.

## Extending the Project

You can extend this project by:
- Adding more tools to existing servers
- Creating new servers (e.g., API server, file system server)
- Implementing HTTP transport for remote access
- Adding authentication and authorization
- Implementing more complex workflows
- Adding error handling and validation
- Creating a web interface for the servers

## Resources

- [MCP Documentation](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

## License

This is an educational project. Feel free to use and modify as needed.


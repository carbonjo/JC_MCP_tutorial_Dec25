# Testing Ollama MCP Tools

## What Are Ollama MCP Tools?

When Ollama shows "13 tools enabled" in the "Tools & MCP" section, it means Ollama has built-in MCP (Model Context Protocol) tools that allow you to:
- List available models (`ollama_list`)
- Pull models (`ollama_pull`)
- Chat with models (`ollama_chat`)
- Generate embeddings (`ollama_embed`)
- And more...

These are **different** from your custom MCP servers (`code_server.py`, `database_server.py`, `document_server.py`).

## How to Verify Ollama MCP Tools Are Working

### Method 1: Quick Test Script

Run the test script:

```bash
cd /Users/carbonjo/Library/CloudStorage/Dropbox/AI/Agents-Langchain-llamaindex-MCP/MCP_Nov29-25
python test_ollama_mcp.py
```

This will:
1. Connect to the Ollama MCP server
2. List all available tools
3. Test a few key tools (list models, check running models, etc.)

### Method 2: Manual Testing via Ollama CLI

If you have Ollama installed, you can test directly:

```bash
# Check if Ollama is running
ollama list

# Pull a model (if not already pulled)
ollama pull llama3

# Test a chat
ollama run llama3 "Hello, are MCP tools working?"
```

### Method 3: Test via Python (Using Ollama Python Library)

```python
import ollama

# Test 1: List models
print("Available models:")
response = ollama.list()
for model in response.models:
    print(f"  - {model.model}")

# Test 2: Check running models
print("\nRunning models:")
response = ollama.ps()
if response.models:
    for model in response.models:
        print(f"  - {model.name}")
else:
    print("  (none)")

# Test 3: Simple chat
print("\nTesting chat:")
response = ollama.chat(
    model="llama3",
    messages=[{"role": "user", "content": "Say 'MCP tools are working!'"}]
)
print(f"Response: {response['message']['content']}")
```

### Method 4: Test via MCP Client (If Configured)

If you have Ollama MCP server configured in your MCP client (like Cursor, Claude Desktop, etc.):

1. **In Cursor/Claude Desktop**: The tools should appear automatically when Ollama MCP is configured
2. **Check the MCP configuration file** (usually `~/.config/mcp.json` or similar)
3. Look for Ollama MCP server configuration

## Troubleshooting

### Issue: "ollama-mcp command not found"

**Solution**: The Ollama MCP server might be integrated differently. Check:

1. **If using Ollama Desktop**: The MCP tools might be built-in and don't need a separate command
2. **If using command-line Ollama**: You might need to install the MCP server separately:
   ```bash
   npm install -g @modelcontextprotocol/server-ollama
   ```

### Issue: "Connection refused" or "Cannot connect"

**Solutions**:
1. Make sure Ollama is running:
   ```bash
   ollama serve
   ```
   Or check if Ollama Desktop is running

2. Check if Ollama is accessible:
   ```bash
   curl http://localhost:11434/api/tags
   ```

3. Verify the MCP server command:
   - It might be `npx @modelcontextprotocol/server-ollama` instead of `ollama-mcp`
   - Or it might be integrated into Ollama itself

### Issue: "Tools show but don't work"

**Check**:
1. Are models pulled? Run `ollama list` to see available models
2. Is Ollama running? Check `ollama ps` to see running models
3. Check Ollama logs for errors

## Understanding the 13 Tools

The 13 Ollama MCP tools typically include:

1. **ollama_list** - List available models
2. **ollama_pull** - Download a model
3. **ollama_chat** - Chat with a model
4. **ollama_generate** - Generate text completion
5. **ollama_embed** - Generate embeddings
6. **ollama_ps** - List running models
7. **ollama_show** - Show model details
8. **ollama_copy** - Copy a model
9. **ollama_delete** - Delete a model
10. **ollama_push** - Push model to registry
11. **ollama_create** - Create a custom model
12. **ollama_web_search** - Web search (if configured)
13. **ollama_web_fetch** - Fetch web pages (if configured)

## Quick Verification Checklist

- [ ] Ollama is installed and running
- [ ] At least one model is pulled (`ollama list` shows models)
- [ ] MCP tools show "13 tools enabled" in Ollama interface
- [ ] Test script can connect (if using MCP client)
- [ ] Basic Ollama commands work (`ollama list`, `ollama run`)

## Next Steps

Once verified:
1. Use Ollama MCP tools in your applications
2. Integrate with your custom MCP servers
3. Build agents that combine Ollama models with your MCP tools

## Need Help?

If the test script doesn't work, check:
1. The exact command for your Ollama MCP server (might be different)
2. Whether Ollama MCP is built into Ollama Desktop vs. separate installation
3. Your MCP client configuration (Cursor, Claude Desktop, etc.)


# Getting Started Guide

## Overview

This project has **two notebooks** that demonstrate MCP (Model Context Protocol):

1. **`mcp_client_demo.ipynb`** - Basic MCP demo (START HERE)
2. **`mcp_llm_agent.ipynb`** - Advanced LLM integration (run after understanding the basics)

## How It Works

### Architecture

```
┌─────────────┐
│  Jupyter    │
│  Notebook   │  (Client)
└──────┬──────┘
       │
       │ Spawns & Communicates via stdio
       │
       ▼
┌─────────────┐
│ MCP Servers │  (code_server.py, database_server.py, document_server.py)
└─────────────┘
```

**Key Points:**
- The **notebook** is the **client**
- The **servers** are **automatically spawned** when you connect
- Communication happens via **stdio** (standard input/output)
- No need to manually start servers - they start automatically!

### Execution Order

#### Step 1: Start with `mcp_client_demo.ipynb`

This notebook shows the basics:
1. **Run Cell 1**: Import libraries
2. **Run Cell 2**: Demo Code Server (writes files, executes code)
3. **Run Cell 3**: Demo Database Server (queries SQLite)
4. **Run Cell 4**: Demo Document Server (manages documents)
5. **Run Cell 5**: Combined workflow

**Important:** Run cells **one at a time** and wait for each to complete.

#### Step 2: Then try `mcp_llm_agent.ipynb`

This notebook adds LLM intelligence:
1. **Run Cell 1**: Import libraries
2. **Run Cell 2**: Connect to MCP servers
3. **Run Cell 3**: Set up Ollama (local LLM) or API keys
4. **Run Cell 4**: Use intelligent agent

## Understanding `await` in Jupyter

### Why `await` works in Jupyter

Jupyter/IPython has **built-in support for top-level `await`**. This means you can use `await` directly in cells without wrapping in `asyncio.run()`.

### What happens when you run a cell with `await`

1. **Cell starts**: Shows `[*]` (running)
2. **Async function executes**: Connects to MCP server
3. **Server spawns**: Python process starts automatically
4. **Communication**: Client and server communicate via stdio
5. **Cell completes**: Shows `[1]`, `[2]`, etc. with output

### If cells seem "pending"

If a cell shows `[*]` and never completes:

1. **Check for errors**: Look at the output - there might be an error message
2. **Check server paths**: Make sure you're running from the `notebooks/` directory
3. **Check Python path**: The servers need to find the MCP library
4. **Interrupt kernel**: Press `Ctrl+C` or `Cmd+C` to stop
5. **Restart kernel**: `Kernel` → `Restart` and try again

## Common Issues

### Issue 1: "Connection closed" error

**Cause:** Server process failed to start or crashed

**Solution:**
- Check that you're in the `notebooks/` directory
- Verify server files exist: `../servers/code_server.py`
- Check Python can import `mcp`: `import mcp` should work

### Issue 2: Cell hangs with `[*]`

**Cause:** Server is waiting or there's a deadlock

**Solution:**
- Interrupt the kernel: `Ctrl+C` / `Cmd+C`
- Restart kernel: `Kernel` → `Restart`
- Check if server process is still running (might need to kill it)

### Issue 3: Path errors

**Cause:** Relative paths don't work from wrong directory

**Solution:**
- Always run notebooks from the `notebooks/` directory
- Or use absolute paths in the notebook

## Quick Start Checklist

- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Navigate to project directory
- [ ] Start Jupyter: `jupyter notebook` or `jupyter lab`
- [ ] Open `notebooks/mcp_client_demo.ipynb`
- [ ] Run cells **one at a time**
- [ ] Wait for each cell to complete before running the next
- [ ] If errors occur, read the error message and check this guide

## Tips

1. **Run cells sequentially**: Don't run all cells at once
2. **Read the output**: Error messages tell you what's wrong
3. **Check execution numbers**: `[1]`, `[2]` means cell completed
4. **Use `[*]` as indicator**: Means cell is running
5. **Restart if stuck**: `Kernel` → `Restart` clears everything

## Next Steps

After successfully running `mcp_client_demo.ipynb`:
1. Try `mcp_llm_agent.ipynb` for LLM integration
2. Modify the code to experiment
3. Read the server code to understand how MCP works
4. Create your own MCP servers!


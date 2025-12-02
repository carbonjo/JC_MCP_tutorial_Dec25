# Troubleshooting: "Connection closed" Error

## The Problem

If you see this error:
```
mcp.shared.exceptions.McpError: Connection closed
```

This means the MCP server started but immediately closed the connection. The most common cause is:

## Root Cause: Wrong Python Interpreter

The server is being spawned with the **system Python** instead of the **virtual environment Python** that has MCP installed.

### How to Fix

The notebooks have been updated to automatically use the correct Python interpreter. Make sure:

1. **You're using the updated notebooks** - They now use `PYTHON_EXECUTABLE = sys.executable`
2. **You're running from the venv** - Make sure Jupyter is using the virtual environment
3. **Restart the kernel** - After updating the notebook, restart: `Kernel` → `Restart`

### Verify Your Setup

Run this in a notebook cell to check:
```python
import sys
print(f"Python: {sys.executable}")
print(f"Should be in venv: {sys.executable}")

# Check if MCP is installed
try:
    import mcp
    print("✓ MCP is installed")
except ImportError:
    print("✗ MCP is NOT installed - run: pip install mcp")
```

### Other Possible Causes

1. **Server script has syntax errors**
   - Test: `python servers/code_server.py` (should hang, not crash)
   - Press Ctrl+C to stop

2. **Missing dependencies**
   - Check: `pip list | grep mcp`
   - Reinstall: `pip install -r requirements.txt`

3. **Wrong working directory**
   - Make sure you're running from `notebooks/` directory
   - Or use absolute paths

4. **Python version mismatch**
   - Server needs Python 3.8+
   - Check: `python --version`

### Quick Fix Steps

1. **Restart Jupyter kernel**: `Kernel` → `Restart`
2. **Re-run the first cell** (imports) to set `PYTHON_EXECUTABLE`
3. **Re-run the server connection cell**
4. **Check the output** - Should show "Using Python: /path/to/venv/bin/python"

### Still Not Working?

1. **Check server manually**:
   ```bash
   cd /path/to/project
   source venv/bin/activate  # or activate your venv
   python servers/code_server.py
   ```
   - Should hang (waiting for stdio input)
   - If it crashes, there's an error in the server code

2. **Check MCP installation**:
   ```bash
   python -c "import mcp; print('OK')"
   ```

3. **Verify paths**:
   - Make sure `servers/code_server.py` exists
   - Check file permissions: `ls -l servers/*.py`


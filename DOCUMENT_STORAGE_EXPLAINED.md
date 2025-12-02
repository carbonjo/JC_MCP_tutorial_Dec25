# Document Storage Location Explained

## Where Are My Documents?

When you create a document using the MCP document server, the file is saved in a `documents/` directory. The exact location depends on **where the server process is running**.

## Current Behavior

The document server uses a relative path:
```python
DOCUMENTS_DIR = Path("documents")  # Relative path
DOCUMENTS_DIR.mkdir(exist_ok=True)
```

This means:
- The `documents/` folder is created **relative to the current working directory**
- If you run the notebook from `notebooks/`, files go to `notebooks/documents/`
- If you run from the project root, files would go to `project_root/documents/`

## Your File Location

Based on your setup, your document `test.txt` is located at:
```
notebooks/documents/test.txt
```

You can verify this by:
1. Looking in the `notebooks/` folder in your file explorer
2. Running this in a notebook cell:
   ```python
   import os
   from pathlib import Path
   docs_dir = Path("documents")
   print(f"Documents directory: {docs_dir.absolute()}")
   if docs_dir.exists():
       print(f"Files in documents/: {list(docs_dir.glob('*.txt'))}")
   ```

## Why This Happens

The document server runs as a separate process (via stdio), and its working directory is determined by:
1. Where the Python process starts
2. The current working directory when the notebook kernel was launched

Since Jupyter notebooks typically run from the `notebooks/` directory, that's where the `documents/` folder gets created.

## How to Find Your Documents

### Method 1: Check the notebooks directory
```bash
ls notebooks/documents/
```

### Method 2: Use Python to find them
```python
from pathlib import Path
import os

# Check current working directory
print(f"Current working directory: {os.getcwd()}")

# Check for documents folder
docs_paths = [
    Path("documents"),
    Path("../documents"),
    Path("notebooks/documents"),
    Path("../notebooks/documents"),
]

for path in docs_paths:
    if path.exists():
        print(f"✓ Found documents at: {path.absolute()}")
        print(f"  Files: {list(path.glob('*.txt'))}")
```

### Method 3: Use the document server's list tool
```python
# In your notebook, use the MCP tool to list documents
result = await call_mcp_tool(DOC_SERVER_PARAMS, "list_documents", {})
print(result)
```

## Changing the Storage Location

If you want documents stored in a specific location, you can modify the document server:

### Option 1: Use Absolute Path (Recommended)
Edit `servers/document_server.py`:
```python
# Change from:
DOCUMENTS_DIR = Path("documents")

# To:
DOCUMENTS_DIR = Path(__file__).parent.parent / "documents"  # Project root
# Or:
DOCUMENTS_DIR = Path.home() / "mcp_documents"  # Home directory
```

### Option 2: Use Environment Variable
```python
import os
DOCUMENTS_DIR = Path(os.getenv("MCP_DOCUMENTS_DIR", "documents"))
```

Then set the environment variable:
```bash
export MCP_DOCUMENTS_DIR="/path/to/your/documents"
```

## Summary

- ✅ Your document **was created successfully**
- 📁 Location: `notebooks/documents/test.txt`
- 🔍 The file contains the summary of "The Prince" by Machiavelli
- 💡 Documents are stored relative to where the server process runs

To view your document:
```python
# Read it using the MCP tool
result = await call_mcp_tool(DOC_SERVER_PARAMS, "read_document", {"name": "test"})
print(result)
```

Or open it directly:
```python
from pathlib import Path
doc_path = Path("documents/test.txt")
if doc_path.exists():
    print(doc_path.read_text())
else:
    print(f"File not found at {doc_path.absolute()}")
```


# Jupyter Notebook Troubleshooting

## Issue: Execution Numbers and Timestamps Not Showing

If you don't see cell execution numbers (like `[1]`, `[2]`, etc.) or timestamps after running cells, here's how to fix it:

### JupyterLab

1. **Enable Line Numbers:**
   - Go to: `View` → `Show Line Numbers`
   - Or: Right-click on a cell → `Show Line Numbers`

2. **Enable Execution Time:**
   - Go to: `Settings` → `Advanced Settings Editor`
   - Select: `Notebook` in the left panel
   - Find: `showExecutionTime` setting
   - Set to: `true`
   - Click: `Save User Settings`

3. **Alternative Method:**
   - Open Settings: `Settings` → `Notebook`
   - Enable: "Show execution time"

### Jupyter Notebook (Classic)

Execution numbers should appear automatically. If they don't:

1. **Check if cells are actually executing:**
   - Look for `[*]` which means cell is running
   - After execution, it should show `[1]`, `[2]`, etc.

2. **Restart kernel:**
   - `Kernel` → `Restart`
   - Then run cells again

3. **Clear output and re-run:**
   - `Cell` → `All Output` → `Clear`
   - Then run cells again

### VS Code Jupyter Extension

1. **Open Settings:**
   - `File` → `Preferences` → `Settings`
   - Search for: "jupyter"

2. **Enable execution display:**
   - Find: `Jupyter: Show Variable View When Debugging`
   - Check: `Jupyter: Enable Cell Execution Timestamps`

3. **Or edit settings.json:**
   ```json
   {
     "jupyter.showVariableViewWhenDebugging": true,
     "jupyter.enableCellExecutionTimestamps": true
   }
   ```

### Google Colab

Execution numbers appear automatically in Colab. If they don't:
- Refresh the page
- Make sure you're running cells (not just viewing)

### General Solutions

1. **Restart Jupyter:**
   ```bash
   # Stop current server (Ctrl+C)
   # Then restart
   jupyter notebook
   # or
   jupyter lab
   ```

2. **Update Jupyter:**
   ```bash
   pip install --upgrade jupyter jupyterlab notebook
   ```

3. **Check notebook metadata:**
   - The notebook should have proper metadata
   - Execution counts should update when cells run
   - If cells show `[*]` but never complete, there's an error

4. **Clear browser cache:**
   - Sometimes browser cache can cause display issues
   - Try: Hard refresh (Ctrl+Shift+R or Cmd+Shift+R)

### Verify It's Working

After applying fixes, you should see:
- Cell numbers like `[1]`, `[2]`, `[3]` after execution
- `[*]` while a cell is running
- Execution time (if enabled) showing how long each cell took

### Still Not Working?

1. **Check Jupyter version:**
   ```bash
   jupyter --version
   ```

2. **Try a different browser:**
   - Sometimes browser extensions interfere

3. **Check for errors:**
   - Look in browser console (F12)
   - Check Jupyter server logs

4. **Reinstall Jupyter:**
   ```bash
   pip uninstall jupyter jupyterlab notebook
   pip install jupyter jupyterlab notebook
   ```

## Quick Fix Commands

```bash
# Generate Jupyter config (if needed)
jupyter notebook --generate-config

# Or for JupyterLab
jupyter lab --generate-config

# Then edit the config file to enable execution display
```


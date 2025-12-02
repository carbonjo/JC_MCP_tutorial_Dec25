"""
Jupyter Notebook Configuration
This file helps ensure execution numbers and timestamps are displayed.
Place this in: ~/.jupyter/jupyter_notebook_config.py
Or run: jupyter notebook --generate-config
"""

# Enable execution timestamps
c = get_config()

# Show execution numbers
c.NotebookApp.show_execution_time = True

# Enable cell execution timestamps
c.NotebookApp.iopub_data_rate_limit = 10000000

# Display cell execution count
c.NotebookApp.allow_origin = '*'

# For JupyterLab, these settings are in the UI:
# Settings → Advanced Settings Editor → Notebook → showExecutionTime: true


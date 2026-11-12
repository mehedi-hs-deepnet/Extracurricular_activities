"""
app.py
------
Root entrypoint for Streamlit.
Executes main/app.py on every rerun so that widget interactions,
Ctrl+Enter submissions, and button clicks never result in a blank screen.
"""

import os
import sys

# Ensure root path is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Dynamically compile and execute main/app.py on every rerun
script_path = os.path.join(BASE_DIR, "main", "app.py")
with open(script_path, "r", encoding="utf-8") as f:
    code = compile(f.read(), script_path, "exec")
    exec(code, globals())

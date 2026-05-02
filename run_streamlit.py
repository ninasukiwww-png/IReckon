import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from streamlit.web import bootstrap

if __name__ == "__main__":
    base = Path(__file__).parent
    script = base / "ui" / "app.py"
    flag_options = {
        "server.port": 8501,
        "server.headless": True,
        "browser.serverAddress": "localhost",
        "browser.gatherUsageStats": False,
    }
    bootstrap.run(str(script), is_hello=False, args=[], flag_options=flag_options)
from pathlib import Path
import os
import sys

# Allow examples to run directly from a source checkout without installation.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def finish_smoke(root):
    if os.environ.get("TKINTER_DASH_SMOKE"):
        root.after(80, root.destroy)

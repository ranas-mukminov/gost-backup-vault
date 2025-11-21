import sys
from pathlib import Path


# Ensure the project src/ directory is importable when running tests without
# installing the package first.
ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

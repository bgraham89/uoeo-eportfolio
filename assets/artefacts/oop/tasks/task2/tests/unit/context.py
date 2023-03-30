from pathlib import Path
import sys

path = Path(__file__).resolve().parent.parent.parent
sys.path.insert(path)

import sample
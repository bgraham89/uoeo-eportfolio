'''
Helper file for making imports convenient.

Provides correct context to imports. 
main.py and tests/context.py imports through this 
module. No other files do, to prevent circular imports.
'''

from pathlib import Path
import sys

path = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(path))

from app.helperfunctions import converters, guards
from app.imports import components, datastructures, models
from app.network.config import addresses, protocols
from app.ui import tui
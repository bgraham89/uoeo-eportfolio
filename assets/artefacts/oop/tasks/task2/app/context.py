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

import app.imports.components as components
import app.imports.datastructures as datastructures
import app.helperfunctions.converters as converters
import app.helperfunctions.guards as guards
import app.imports.models as models
import app.network.config.addresses as addresses
import app.network.config.protocols as protocols
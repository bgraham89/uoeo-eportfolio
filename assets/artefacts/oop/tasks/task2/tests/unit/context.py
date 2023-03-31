'''
Helper file for making imports convenient.

Provides correct context to siblings when importing app packages. 
Siblings should import this module. 
'''

from pathlib import Path
import sys

path = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(path))

import app.components as components
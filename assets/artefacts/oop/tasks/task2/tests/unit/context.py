'''
Helper file for making imports convenient.

Provides correct context to test imports. 
test_.py files import through this module. 
'''

from pathlib import Path
import sys

path = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(path))

from app.context import components, datastructures, guards
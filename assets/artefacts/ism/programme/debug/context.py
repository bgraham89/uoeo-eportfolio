'''Helper file for imports'''

from pathlib import Path
import sys

path = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(path))

from datastructures.node import Node, NodeDictionary, NodeParamaters
from datastructures.tree import Tree
from STIX.parser import STIXParser

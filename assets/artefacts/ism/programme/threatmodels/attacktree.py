from datastructures.tree import Tree
from STIX.parser import STIXParser

class AttackTree(Tree):
    def __init__(self, datapath, id="", description="", values=""):
        parser = STIXParser(mode="attack_tree")
        params_array = parser(datapath)
        values = values or {}
        values["type"] = "attack-tree"
        super().__init__(id=id, description=description, values=values,
                         node_paramaters_array=params_array)
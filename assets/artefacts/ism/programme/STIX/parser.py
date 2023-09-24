from datastructures.node import NodeParamaters
from datastructures.tree import Tree
import json

class STIXParser(object):
    def __init__(self, mode="attack_tree"):
        self._mode = mode
        self._data = {}

    def __call__(self, filepath):
        if self._mode == "attack_tree":
            return self.create_attack_tree_params(filepath)
        else:
            raise UnknownUsecaseError(f"{self._mode=} which is not recognised.")

    @property
    def mode(self):
        return self._mode
    
    @mode.setter
    def mode(self, mode):
        self._mode = mode

    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, *args, **kwargs):
        raise PermissionError("Currently not supported.")
        
    def create_attack_tree_params(self, filepath):
        with open(filepath) as file:
            self._data = json.load(file)

        node_params_array = []
        
        # groupings preprocessing
        groupings = list(filter(lambda x : x["type"] == "grouping", self._data))
        groupings_childmap = {group["name"] : group["object_refs"] for group in groupings}
        # attack_patterns preprocessing
        aps = list(filter(lambda x : x["type"] == "attack-pattern", self._data))
        aps_not_leaves = filter(lambda x : "object_refs" in x, aps)
        aps_childmap = {ap["name"] : ap["object_refs"] for ap in aps_not_leaves}
        aps_idmap = {ap["id"] : ap["name"] for ap in aps}
        
        # grouping nodes paramaters
        for g in groupings:
            id = g["name"]
            description = g["description"]
            values = {"type" : g["type"]}
            parent_id = Tree.ROOT_ID()
            child_ids = [aps_idmap[c] for c in groupings_childmap[id]]
            node_params = NodeParamaters(id, description, values, parent_id, child_ids)
            node_params_array.append(node_params)
        # attack_pattern nodes paramaters
        for ap in aps:
            id = ap["name"]
            description = ap["description"]
            values = {"type" : ap["type"]}
            parent_id = ""
            is_leaf = ap["name"] in aps_childmap
            child_ids = [aps_idmap[c] for c in aps_childmap[id]] if is_leaf else []
            node_params = NodeParamaters(id, description, values, parent_id, child_ids)
            node_params_array.append(node_params)
        
        return node_params_array

class UnknownUsecaseError(BaseException):
    '''Raised when a STIXParser cannot determine an algorithm to create NodeParams.'''
    pass
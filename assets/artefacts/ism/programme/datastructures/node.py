class Node(object):
    def __init__(self, id, description=""):
        '''Used as a node for a tree.'''
        # node contents
        self._id = id
        self._description = description
        self._values = dict()
        # branching information
        self._parent_node = None
        self._child_nodes = NodeDictionary()

    def __repr__(self):
        has_no_parent = self._parent_node == None
        parent_str = None if has_no_parent else self._parent_node.id
        return (f"Node(id={self._id}, description={self._description}, " +
               f"values={self._values}, parent_node={parent_str}, " +
               f"num_child_nodes={len(self._child_nodes)})")

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, *args, **kwargs):
        raise PermissionError("Node id cannot be updated.")
    
    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description
    
    @property
    def values(self):
        return self._values
    
    @values.setter
    def values(self, values):
        try:
            assert type(values) is dict
        except:
            print(f"Unexpected {values=}")
            raise TypeError(f"Node values must be stored in a dictionary.")
        self._values = values

    @property
    def parent_node(self):
        return self._parent_node
    
    @parent_node.setter
    def parent_node(self, parent_node):
        try:
            assert isinstance(parent_node, Node) or parent_node == None
        except:
            raise TypeError("Node parent_node must be a Node object.")
        self._parent_node = parent_node
        
    @property
    def child_nodes(self):
        return self._child_nodes
    
    @child_nodes.setter
    def child_nodes(self, child_nodes):
        try:
            assert isinstance(child_nodes, NodeDictionary)
        except:
            raise TypeError("Node child_nodes must be stored in a NodeDictionary object.")
        self._child_nodes = child_nodes
        


class NodeDictionary(dict):
    '''Used to assert Tree only contains Node objects.'''

    def __setitem__(self, __key, __value):
        try:
            assert isinstance(__value, Node)
        except:
            raise TypeError("A NodeDictionary can only store Node objects.")
        return super().__setitem__(__key, __value)



class NodeParamaters(dict):
    '''Used as a container for holding Node object creation and connection paramaters.'''

    def __init__(self, id, description="", values="", parent_id="", child_ids=""):
        self["id"] = id
        self["description"] = description
        self["values"] = values or {}
        self["parent_id"] = parent_id
        self["child_ids"] = child_ids or []

    def __str__(self):
        id, description, values, parent_id, child_ids = (
            self.id, self.description, self.values, self.parent_id, self.child_ids)
        return f"NodeParamaters: \n{id=}, \n{description=}, \n{values=}, \n{parent_id=}, \n{child_ids}"

    @property
    def id(self):
        return self["id"]
    
    @property
    def description(self):
        return self["description"]
    
    @property
    def values(self):
        return self["values"]
    
    @property
    def parent_id(self):
        return self["parent_id"]

    @property
    def child_ids(self):
        return self["child_ids"]
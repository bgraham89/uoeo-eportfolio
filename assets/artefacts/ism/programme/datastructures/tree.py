from datastructures.node import Node, NodeDictionary, NodeParamaters

class Tree(NodeDictionary):
    '''Used to encapsulate tree operations.'''
    _ROOT_ID = "root"

    def __init__(self, id, description="", values="", root_node_id="", 
                 root_node_description="", root_node_values="",
                 node_paramaters_array=""):
        # tree details (not related to nodes)
        self._id = id
        self._description = description
        self._values = values or {}
        # root node
        self._root_node = self.create_root_node(root_node_id, root_node_description, root_node_values)
        # remaining nodes
        nodes = self.create_nodes_from_params_array(node_paramaters_array)
        self.update({node.id : node for node in nodes})
        self.connect_nodes_from_params_array(node_paramaters_array)

    @classmethod
    def ROOT_ID(cls):
        return cls._ROOT_ID

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, *args, **kwargs):
        raise PermissionError("Tree id cannot be updated.")
    
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
            raise TypeError("Tree values must be stored in a dictionary.")
        self._values = values
        
    @property
    def root_node(self):
        return self._root_node
    
    @root_node.setter
    def root_node(self, *args, **kwargs):
        raise PermissionError("Root node cannot be replaced.")
        
    def create_node_from_params(self, params):
        '''Takes a NodeParamaters object and returns a Node object.'''
        id = params.id
        description = params.description or ""
        values = params.values or {}

        node = Node(id, description)
        node.values = values

        return node
    
    def create_root_node(self, id, description, values):
        id = id or self._ROOT_ID
        try:
            params = NodeParamaters(id, description, values)
            root = self.create_node_from_params(params)
            self[id] = root
            root.values["type"] = "root"
        except Exception as err:
            print("Failed to create root_node of the Tree.")
            print(f"Unexpected {id=}, {description=}, {values=}")
            raise(err)
        
        return root
    
    def connect_nodes(self, child_node, parent_node, strict=True):
        '''Connects two Node objects, strict flag asserts acyclic relationships.'''
        if parent_node.id not in self:
            raise MissingNodeError(f"Node with {parent_node.id=} is referenced but doesn't exist.")
        if child_node.id not in self:
            raise MissingNodeError(f"Node with {child_node.id=} is referenced but doesn't exist.")

        if strict:
            if parent_node.parent_node == child_node:
                raise AncestoryCycleError(f"Parent of parent node is the child node.")
            if parent_node.id in child_node.child_nodes:
                raise AncestoryCycleError(f"Child of child node is it's parent.")

        child_node.parent_node = parent_node
        parent_node.child_nodes[child_node.id] = child_node

    def create_nodes_from_params_array(self, params_array):
        '''Takes an array of NodeParamaters and creates Node objects.'''
        nodes = []
        params_array = params_array or []
        for params in params_array:
            try:
                assert isinstance(params, NodeParamaters)
                nodes.append(self.create_node_from_params(params))
            except AssertionError:
                print("Node paramaters must be stored in a a NodeParamaters objects")
            except Exception as err:
                print("Failed to create node", params)
                raise(err)
    
        return nodes
    
    def connect_nodes_from_params_array(self, params_array):
        '''Connect Tree nodes using ancestory relationships of NodeParamaters array'''
        params_array = params_array or [] 
        for params in params_array:
            node = self[params.id]
            if params.parent_id:
                self.connect_nodes(node, self[params.parent_id], strict=True)
            if params.child_ids:
                for child_id in params.child_ids:
                    self.connect_nodes(self[child_id], node, strict=True)

    def add_value_to_node(self, node_id, keyword, value, aggregate=False):
        '''Add a keyword : value pair to a node'''
        if aggregate:
            result = 0
            node = self[node_id]
            children = node.child_nodes.values()
            for child in children:
                if keyword in child.values:
                    value = child.values[keyword]
                    if value.isdigit():
                        result += int(value)
            self[node_id].values[keyword] = result 
        else:
            self[node_id].values[keyword] = value  



class MissingNodeError(BaseException):
    '''Raised when a node is referred to that doesn't exist in the tree.'''
    pass


class AncestoryCycleError(BaseException):
    '''Raised when the parent of a node is also it's child.'''
    pass

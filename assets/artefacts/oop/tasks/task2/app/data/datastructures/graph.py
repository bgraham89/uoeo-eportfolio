'''A graph datastructure'''

from app.helperfunctions import guards
from collections.abc import Hashable
from math import inf

class Graph(object):
    '''A collection of nodes and edges connecting them.'''
    def __init__(self):
        self._nodes = set()
        self._edges = {}

    def __repr__(self):
        return f"Graph(\nnodes={self._nodes})"

    def add_node(self, node):
        '''Add node to the graph'''
        guards.arg_cond((node,), self._node_constraints())
        self._nodes.add(node)

    def add_nodes(self, nodes):
        '''Add multiple nodes to the graph'''
        for node in nodes:
            self.add_node(node)

    def add_directed_edge(self, node_i, node_ii):
        '''Add directed edge to the graph from one node to other'''
        guards.arg_cond((node_i, node_ii), self._edge_constraints())
        self._edges.setdefault(node_i, set())
        self._edges[node_i].add(node_ii)

    def add_undirected_edge(self, node_i, node_ii):
        '''Add undirected edge to the graph from one node to other'''
        self.add_directed_edge(node_i, node_ii)
        self.add_directed_edge(node_ii, node_i)  #minutely inefficient

    def shortest_path(self, node_start, node_end):
        ''' Calculates the shortest path between two nodes'''
        def _djikstra(self, current_node):
            '''Recursive search by bredth check from closest node'''
            for next_node in self._edges[current_node]:
                if node_end in self._edges[current_node]:
                    breadcrumbs[next_node] = current_node
                    return True  #path found
                else:
                    current_distance = distances[current_node] + 1
                    if current_distance < distances[next_node]:
                        distances[next_node] = current_distance
            unvisited_nodes.remove(current_node)
            closest_unvisited = sorted(list(unvisited_nodes), sort_closest)
            if distances[closest_unvisited] == inf:
                return False  #path impossible
            else:
                breadcrumbs[closest_unvisited[0]]
                return _djikstra(closest_unvisited[0])  #keep looking 
        distances = {node : inf for node in self._nodes}
        sort_closest = lambda x, y : distances[x] <= distances[y]
        breadcrumbs = {node : None for node in self._nodes}
        unvisited_nodes = set(distances.keys())
        distances[node_start] = 0
        if _djikstra(node_start):
            path = [node_end]
            while node_prev := breadcrumbs[node_end]:
                path.append(node_prev)
                node_end = node_prev
            return path
        else:
            return []

    def _node_constraints(self):
        '''Assertion conditions for nodes'''
        def hashable(x):
            '''Checks that node can be stored in set'''
            has_hash = isinstance(x, Hashable)
            has_eq = hasattr(x, '__eq__')
            return has_hash and has_eq
        def unique(x):
            '''Checks node isnt stored already'''
            return x not in self._nodes
        return lambda x : hashable(x) and unique(x)
    
    def _edge_constraints(self):
        '''Assertion conditions for edges'''
        def relevant(x):
            '''Checks that node is in graph'''
            return x in self._nodes
        return lambda x, y : relevant(x) and relevant(y)
    
    @classmethod
    def Null(cls, nodes):
        '''Make a Graph with nodes, but no edges.'''
        graph = cls()
        graph.add_nodes(nodes)
        return graph

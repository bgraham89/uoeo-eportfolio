import app.datastructures as avds
import logging
from random import shuffle
import traceback

class Map(object):
    '''A class to represent a road map.'''
    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._grid = [self.int_to_coord(n) for n in range(width * height)]
        self._graph = None

    def int_to_coord(self, n):
        '''Converts an int to Cartesian Coordinates.'''
        x = n % self._width
        y = n // self._height
        return (x, y)
    
    def coord_to_int(self, coord):
        '''Converts Cartesian Coordinates to an int.'''
        x, y = coord
        n = (y * self._height) + x
        return n

    @classmethod
    def RandomSpanningTree(cls, width, height):
        '''Generates a spanning tree to overlay a grid of points'''
        map = cls(width, height)
        nodes = [map.coord_to_int(coord) for coord in map._grid]
        map._graph = avds.Graph.Null(nodes)
        # potential edges enumerated per orientation, arithemtically
        horiz_cond = lambda x : x // height == (x+1) // height
        vert_cond = lambda x : x + height < width * height
        horiz_edges = [(node, node + 1) for node in nodes if horiz_cond(node)]
        vert_edges = [(node, node + height) for node in nodes if vert_cond(node)]
        pot_edges = horiz_edges + vert_edges
        # Kruskal's algorithm for maze / spanning tree generation
        islands = {node : set((node,)) for node in nodes}
        shuffle(pot_edges)
        for a, b in pot_edges:
            if b not in islands[a]:
                island = islands[a].union(islands[b])
                for node in island:
                    islands[node] = island
            map._graph.add_undirected_edge(a,b)
            if len(island) == len(nodes):
                return map
        else:
            logging.error(traceback.format_exc())  #educational
            err_message = "Edges were not enumerated properly."
            raise Exception(err_message)
            


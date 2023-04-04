from random import shuffle

class Map(object):
    '''A class to represent roads'''
    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._grid = [self.int_to_coord(n) for n in range(width * height)]
        self._graph = None

    def int_to_coord(self, n):
        '''converts an int to a point on the grid'''
        x = n % self._width
        y = n // self._height
        return (x, y)

    @classmethod
    def generate__random(cls, width, height):
        '''generates a spanning tree for a grid'''
        map = cls(width, height)
        points = [n for n in range(width * height)]
        map._graph.add_points(points)
        # potential edges enumerated per orientation
        horiz_cond = lambda x : x % height == (x+1) % height
        vert_cond = lambda x : x + height < width * height
        horiz_edges = [(point, point + 1) for point in points if horiz_cond(point)]
        vert_edges = [(point, point + height) for point in points if vert_cond(point)]
        pot_edges = horiz_edges + vert_edges
        # Kruskal's algorithm for maze / spanning tree generation
        islands = {point : set(point) for point in points}
        shuffle(pot_edges)
        for a, b in pot_edges:
            if b not in islands[a]:
                connection = islands[a].union(islands[b])
                for point in connection:
                    islands[point] = connection
            map.add_edge((a,b))
            if len(connection) == len(points):
                break
            


'''Unit tests for classes representing conceptual models'''

from context import models as avm
import unittest

class TestMap(unittest.TestCase):
    '''Unit tests for the Map class.'''

    def setUp(self):
        self.width = 16
        self.height = 16
        self.biggest_node = self.width * self.height - 1

    def test_grid_assigned(self):
        '''Expect grid attribute to match input.'''
        map = avm.Map(self.width, self.height)
        self.assertEqual(len(map._grid), self.width * self.height)

    def test_random_graph_assignment(self):
        '''Expect graph to be assigned to attribute.'''
        map = avm.Map.RandomSpanningTree(self.width, self.height)
        self.assertTrue(map._graph)

    def test_random_graph_has_no_illegal_edge(self):
        '''Expect graph edges to obey arithmetic constraints.'''
        map = avm.Map.RandomSpanningTree(self.width, self.height)
        for node, connected_nodes in map._graph._edges.items():
            for connected_node in connected_nodes:
                if connected_node > node:
                    horiz_cond = node + 1 == connected_node and connected_node % self.width
                    vert_cond = node + self.height == connected_node
                else:
                    horiz_cond = node - 1 == connected_node and node % self.width
                    vert_cond = node - self.height == connected_node
                self.assertTrue(horiz_cond or vert_cond)

    def test_random_graph_spans_whole_grid(self):
        '''Expect path exists between all coords.'''
        map = avm.Map.RandomSpanningTree(self.width, self.height)
        for node in map._graph._nodes:
            if node:
                self.assertTrue(map._graph.shortest_path(0, node))
    
    def test_shortest_path_includes_start_and_end(self):
        '''Expect path contains endpoints'''
        map = avm.Map.RandomSpanningTree(self.width, self.height)
        for node in map._graph._nodes:
            if node:
                path = map._graph.shortest_path(0, node)
                self.assertTrue(0 in path and node in path)
            else:
                path = map._graph.shortest_path(self.biggest_node, 0)

    def test_shortest_path_produces_real_path(self):
        '''Expect path is traversable.'''
        map = avm.Map.RandomSpanningTree(self.width, self.height)
        for node in map._graph._nodes:
            if node:
                path = map._graph.shortest_path(0, node)
                sw = [0, 1]
                while node not in map._graph._edges[path[sw[0]]]:
                    self.assertTrue(path[sw[1]] in map._graph._edges[path[sw[0]]])
                    sw[0] += 1
                    sw[1] += 1

    def test_shortest_path_has_no_dupes(self):
        '''Expect shortest path to have no duplicates.'''
        map = avm.Map.RandomSpanningTree(self.width, self.height)
        for node in map._graph._nodes:
            if node:
                path = map._graph.shortest_path(1, node)
                self.assertEqual(len(path), len(set(path)))

class TestRoadNames(unittest.TestCase):
    '''Unit tests for the Road Names function.'''

    def setUp(self):
        self.num_streets = 50

    def test_names_are_unique(self):
        '''Expect names to contain no duplicates.'''
        names = avm.make_road_names(self.num_streets)
        self.assertEqual(len(names), len(set(names)))




if __name__ == '__main__':
    unittest.main()
'''Unit tests for classes representing conceptual models'''

from context import models as avm
import unittest

class TestMap(unittest.TestCase):
    '''Unit tests for the FixedArray class.'''

    def setUp(self):
        self.width = 16
        self.height = 16

    def test_grid_assigned(self):
        '''Expect grid attribute to match input.'''
        map = avm.Map(self.width, self.height)
        self.assertEqual(len(map._grid), self.width * self.height)

    def test_int_to_coord_converter(self):
        '''Expect coords to increase with int.'''
        map = avm.Map(self.width, self.height)
        for n in range(self.width * self.height):
            coord = map.int_to_coord(n)
            if n:
                x_inc = coord[0] > prev_coord[0]
                y_inc = coord[1] > prev_coord[1]
                self.assertTrue(x_inc or y_inc)
            prev_coord = coord

    def test_coord_to_int_converter(self):
        '''Expect ints unaffected by transformation.'''
        map = avm.Map(self.width, self.height)
        for n in range(self.width * self.height):
            coord = map.int_to_coord(n)
            n_return = map.coord_to_int(coord)
            self.assertEqual(n, n_return)

    def test_random_graph_assignment(self):
        '''Expect graph to be assigned to attribute.'''
        map = avm.Map.RandomSpanningTree(self.width, self.height)
        self.assertTrue(map._graph)

    def test_random_graph_spans(self):
        '''Expect graph to be assigned to attribute.'''
        map = avm.Map.RandomSpanningTree(self.width, self.height)
        self.assertTrue(map._graph)



if __name__ == '__main__':
    unittest.main()
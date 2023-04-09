'''Unit tests for guard helper functions'''

from collections import Counter
from context import converters as conv, guards
import unittest

class TestArgCondGuard(unittest.TestCase):
    '''Unit tests for the arg_condition guard function.'''

    def setUp(self):
        self.x = "dummy_param"
        self.y = "another_dummy_param"

    def test_always_true_condition_on_single_param(self):
        '''Expect True condition to not raise error.'''
        def dummy_function(x):
            guards.arg_cond((x,), lambda x_ : True)
            return x
        self.assertEqual(dummy_function(self.x), self.x)

    def test_always_true_condition_on_multiple_params(self):
        '''Expect True condition to not raise error.'''
        def dummy_function(x, y):
            guards.arg_cond((x, y), lambda x_, y_ : True)
            return x, y
        self.assertEqual(dummy_function(self.x, self.y), (self.x, self.y))

    def test_always_false_condition_on_single_param(self):
        '''Expect False condition to raise AssertionError.'''
        def dummy_function(x):
            guards.arg_cond((x,), lambda x_ : False)
            return x
        with self.assertRaises(AssertionError):
            dummy_function(self.x)

    def test_always_false_condition_on_multiple_params(self):
        '''Expect False condition to raise AssertionError.'''
        def dummy_function(x, y):
            guards.arg_cond((x,y), lambda x_, y_ : False)
            return (x, y)
        with self.assertRaises(AssertionError):
            dummy_function(self.x, self.y)

    def test_too_few_params_for_condition(self):
        '''Expect mismatch to raise TypeError.'''
        def dummy_function(x):
            guards.arg_cond((x,), lambda x_, y_ : True)
            return x
        with self.assertRaises(TypeError):
            dummy_function(self.x)

    def test_too_many_params_for_condition(self):
        '''Expect mismatch to raise TypeError.'''
        def dummy_function(x, y):
            guards.arg_cond((x,y), lambda x : True)
            return (x, y)
        with self.assertRaises(TypeError):
            dummy_function(self.x, self.y)

class TestIntToArrayConverter(unittest.TestCase):
    '''Unit tests for the int_to_array converter function.'''
    
    def setUp(self):
        self.size = 8
        self.powers = (2 ** i for i in range(10))

    def test_powers_encoded_correctly(self):
        '''Expect mathematical pattern to unfold.'''
        for i, power in enumerate(self.powers):
            overflow = i >= 8  # expected pattern breaks for large powers
            zeros = 8 if overflow else 7
            ones = 0 if overflow else 1
            index = None if overflow else zeros - i
            enc = conv.int_to_array(power, self.size)
            counter = Counter(enc)
            self.assertEqual(counter["0"], zeros)
            self.assertEqual(counter["1"], ones)
            if overflow:
                with self.assertRaises(ValueError):
                    enc.index("1")
            else:
                self.assertEqual(enc.index("1"), index)
    
class TestArrayToIntConverter(unittest.TestCase):
    '''Unit tests for the array_to_int converter function.'''

    def setUp(self):
        self.size = 8
        self.powers = (2 ** i for i in range(8))

    def test_powers_encoded_correctly(self):
        '''Expect consistency for inverse.'''
        for power in self.powers:
            array = conv.int_to_array(power, self.size)
            num = conv.array_to_int(array)
            self.assertEqual(num, power)

class TestIntToCoordConverter(unittest.TestCase):
    '''Unit tests for the int_to_array converter function.'''
    def setUp(self):
        self.width = 16
        self.height = 16

    def test_int_to_coord_converter(self):
        '''Expect coords to increase with int.'''
        for n in range(self.width * self.height):
            coord = conv.int_to_coord(n, self.width, self.height)
            if n:
                x_inc = coord[0] > prev_coord[0]
                y_inc = coord[1] > prev_coord[1]
                self.assertTrue(x_inc or y_inc)
            prev_coord = coord

class TestCoordToIntConverter(unittest.TestCase):
    '''Unit tests for the coord_to_int converter function.'''
    def setUp(self):
        self.width = 16
        self.height = 16

    def test_coord_to_int_converter(self):
        '''Expect ints unaffected by transformation.'''
        for n in range(self.width * self.height):
            coord = conv.int_to_coord(n, self.width, self.height)
            n_return = conv.coord_to_int(coord, self.height)
            self.assertEqual(n, n_return) 

if __name__ == '__main__':
    unittest.main()
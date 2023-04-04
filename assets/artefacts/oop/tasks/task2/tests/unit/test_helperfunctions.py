'''Unit tests for guard helper functions'''

from collections import Counter
from context import guards, encoders
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

class TestIntToArrayEncoder(unittest.TestCase):
    '''Unit tests for the int_to_array encoder function.'''
    
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
            enc = encoders.int_to_array(power, self.size)
            counter = Counter(enc)
            self.assertEqual(counter["0"], zeros)
            self.assertEqual(counter["1"], ones)
            if overflow:
                with self.assertRaises(ValueError):
                    enc.index("1")
            else:
                self.assertEqual(enc.index("1"), index)
    
class TestArrayToIntEncoder(unittest.TestCase):
    '''Unit tests for the array_to_int encoder function.'''

    def setUp(self):
        self.size = 8
        self.powers = (2 ** i for i in range(8))

    def test_powers_encoded_correctly(self):
        '''Expect consistency for inverse.'''
        for power in self.powers:
            array = encoders.int_to_array(power, self.size)
            num = encoders.array_to_int(array)
            self.assertEqual(num, power)





if __name__ == '__main__':
    unittest.main()
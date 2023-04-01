'''Unit tests for guard helper functions'''

from context import guards
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

if __name__ == '__main__':
    unittest.main()
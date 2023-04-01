'''Unit tests for guard helper functions'''

from context import datastructures as avds
import unittest

class TestArgCondGuard(unittest.TestCase):
    '''Unit tests for the FixedArray class.'''

    def setUp(self):
        self.size = 32

    def test_size_attribute_created_correctly(self):
        fixed_array = avds.FixedArray(self.size)
        self.assertEqual(len(fixed_array), self.size)

if __name__ == '__main__':
    unittest.main()
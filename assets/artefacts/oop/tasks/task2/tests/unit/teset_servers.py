'''Unit tests for server components'''

from context import components as avc
import unittest

class TestSenseServer(unittest.TestCase):
    '''Unit tests for the FixedArray class.'''

    def setUp(self):
        self.sensor = avc.GPS()

    def test_size_assigned(self):
        '''Expect size attribute to match input.'''
        fixed_array = avds.FixedArray(self.size)
        self.assertEqual(len(fixed_array), self.size)

if __name__ == '__main__':
    unittest.main()
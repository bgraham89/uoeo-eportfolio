'''Unit tests for Sensor objects'''

from context import components as avc
import unittest

class TestGPS(unittest.TestCase):
    '''Unit tests for the GPS class.'''

    def setUp(self):
        self.size = 10
        self.data = ["d", "u", "m", "m", "y", "", "d", "a", "t", "a"]
    
    def test_data_assigned(self):
        '''Expect memory to be updated.'''
        gps = avc.GPS(self.size)
        gps.memory = self.data
        self.assertEqual(gps.memory, self.data)

    def test_data_rejected(self):
        '''Expect assignment to raise AssertionError .'''
        gps = avc.GPS(self.size)
        gps.memory = self.data
        with self.assertRaises(AssertionError):
            gps.memory = self.data + ["!"]
    
    def test_readable(self):
        '''Expect GPS items match data items.'''
        gps = avc.GPS(self.size)
        gps.memory = self.data
        for i in range(self.size):
            self.assertEqual(gps.memory[i], self.data[i])

if __name__ == '__main__':
    unittest.main()
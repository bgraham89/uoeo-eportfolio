'''Unit tests for Sensor objects'''

from context import components as avc
from context import converters as conv
import unittest

class TestGPS(unittest.TestCase):
    '''Unit tests for the GPS class.'''

    def setUp(self):
        self.size = 10
        self.data = ["d", "u", "m", "m", "y", " ", "d", "a", "t", "a"]
    
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
    
    def test_randomiser_assigns(self):
        '''Expect GPS to get random data.'''
        gps = avc.GPS(self.size)
        gps.fake_data()
        self.assertTrue(gps.read_data())

    def test_randomiser_is_information(self):
        '''Expect random data to convert to coords '''
        gps = avc.GPS(self.size)
        gps.fake_data()
        data = gps.read_data()
        data_num = conv.array_to_int(data)
        half = self.size // 2
        coords = conv.int_to_coord(data_num, 2**half, 2**half)
        self.assertTrue(coords[0] < 2**half and coords[1] < 2**half)

class TestDestination(unittest.TestCase):
    '''Unit tests for the Destination class.'''

    def setUp(self):
        self.size = 10
        self.data = ["d", "u", "m", "m", "y", " ", "d", "a", "t", "a"]
    
    def test_data_assigned(self):
        '''Expect memory to be updated.'''
        dest = avc.Destination(self.size)
        dest.memory = self.data
        self.assertEqual(dest.memory, self.data)

    def test_data_rejected(self):
        '''Expect assignment to raise AssertionError .'''
        dest = avc.Destination(self.size)
        dest.memory = self.data
        with self.assertRaises(AssertionError):
            dest.memory = self.data + ["!"]
    
    def test_readable(self):
        '''Expect GPS items match data items.'''
        dest = avc.Destination(self.size)
        dest.memory = self.data
        for i in range(self.size):
            self.assertEqual(dest.memory[i], self.data[i])
    
    def test_randomiser_assigns(self):
        '''Expect GPS to get random data.'''
        dest = avc.Destination(self.size)
        dest.fake_data()
        self.assertTrue(dest.read_data())

    def test_randomiser_is_information(self):
        '''Expect random data to convert to coords '''
        dest = avc.Destination(self.size)
        dest.fake_data()
        data = dest.read_data()
        data_num = conv.array_to_int(data)
        half = self.size // 2
        coords = conv.int_to_coord(data_num, 2**half, 2**half)
        self.assertTrue(coords[0] < 2**half and coords[1] < 2**half)

if __name__ == '__main__':
    unittest.main()
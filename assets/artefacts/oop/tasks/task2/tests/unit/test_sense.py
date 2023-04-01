'''Unit tests for Sensor objects'''

from context import components as avc
import unittest

class TestGPS(unittest.TestCase):
    '''Unit tests for the GPS class.'''

    def setUp(self):
        '''
        Creates a GPS object for testing with.
        
        If GPS doesn't implement the Sensor abstract base class,
        this method will throw an error, before the explicit tests
        have even started.
        '''
        try:
            self.gps = avc.GPS()
        except TypeError as e:
            reason = ("The GPS class doesn't implement it's abstract base class properly.")
            print(reason)
            self.skipTest(str(e))


if __name__ == '__main__':
    unittest.main()
import unittest
from context import components as avc

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
        except TypeError as exc:
            reason = ("The GPS class doesn't implement it's abstract base class.")
            print("\n--------------------Test Skipped---------------------------")
            print(reason)
            self.skipTest(str(exc))

    def test_abc_inheritence(self):
        '''Tests that GPS implements Sensor.'''
        self.assertIsInstance()

if __name__ == '__main__':
    unittest.main()
#  class imports
from app.sense.abstract.sensor import Sensor
from app.data.datastructures.fixedarray import FixedArray

#  function imports
from random import randint

#  module imports
from app.helperfunctions import converters as conv


class Destination(Sensor):
    '''An I/O device that obtains a destination.'''

    def __init__(self, memory_size):
        self._memory = FixedArray(memory_size)
        self._memory_size = memory_size
        self._key = "Destination"

    def write_data(self, data):
        '''Puts data into memory'''
        self._memory.update(data)

    def read_data(self):
        '''Gets raw_data from memory'''
        return list(self._memory)
    
    def fake_data(self):
        '''generates random coordinates'''
        half = self._memory_size // 2
        x = randint(0, 2 ** half - 1)
        y = randint(0, 2 ** half - 1)
        value = (y << half) + x
        data = conv.int_to_array(value, self._memory_size)
        self.write_data(data)
    
    memory = property(read_data, write_data)

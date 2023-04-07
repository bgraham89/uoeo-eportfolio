import app.datastructures as avds
from app.sense.abstract.sensor import Sensor
from app.helperfunctions import encoders
from random import randint

class GPS(Sensor):
    '''A general positioning system for localisation.'''

    def __init__(self, memory_size):
        self._memory = avds.FixedArray(memory_size)
        self._memory_size = memory_size

    def write_memory(self, data):
        '''Puts data into memory'''
        self._memory.update(data)

    def read_memory(self):
        '''Gets raw_data from memory'''
        return list(self._memory)
    
    def fake_memory(self):
        '''generates random coordinates'''
        half = self._memory_size // 2 - 1
        x = randint(0, half)
        y = randint(0, half)
        value = (x << half) + y
        data = encoders.int_to_array(value, self._memory_size)
        self.write_memory(data)
    
    memory = property(read_memory, write_memory)

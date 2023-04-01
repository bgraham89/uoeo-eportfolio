from abc import ABC, abstractmethod

class Sensor(ABC):
    '''
    An abstract base class for a sensor component.
    
    The intent of the class is encapsulate hardware that
    that provides input data to the autonomous vehicle. 
    '''

    @abstractmethod
    def write_memory():
        '''Puts raw_data into memory'''

    @abstractmethod
    def read_memory():
        '''Gets raw_data from memory'''
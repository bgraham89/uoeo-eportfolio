from abc import ABC, abstractmethod

class Server(ABC):
    '''
    An abstract base class for a server component.
    
    The intent of the class is to manage network dynamics
    for hardware. 
    '''

    @abstractmethod
    def make_packages():
        '''Creates package for network transportation'''

    @abstractmethod
    def send_packages():
        '''Sends package to adress'''

    @abstractmethod
    def open_packages():
        '''Deciphers package'''

    
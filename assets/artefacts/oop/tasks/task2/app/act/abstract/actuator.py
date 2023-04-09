from abc import ABC, abstractmethod

class Actuator(ABC):
    '''
    An abstract base class for a actuator component.
    
    The intent of the class is to encapsulate hardware that
    that drives the autonomous vehicle. 
    '''
    @abstractmethod
    def perform_action():
        '''Peforms an action'''
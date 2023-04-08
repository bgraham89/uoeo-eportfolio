from abc import ABC, abstractmethod

class Planner(ABC):
    '''
    An abstract base class for a planner component.
    
    The intent of the class is to encapsulate hardware that
    that provides instructions to the autonomous vehicle. 
    '''

    @abstractmethod
    def make_instruction():
        '''Creates an instruction for another component.'''

    @abstractmethod
    def give_instruction():
        '''Pop instruction off stack.'''

    @abstractmethod
    def clear_instructions():
        '''Clear the instruction stack.'''

    @abstractmethod
    def extract_information():
        '''Extracts information from a packet'''
        
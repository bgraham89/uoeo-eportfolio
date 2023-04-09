'''This class isn't required in this version'''

#  class imports
from app.act.abstract.actuator import Actuator

class Accelerator(Actuator):
    '''An accelerator pedal.'''

    def __init__(self):
        self._key = "Accelerator"

    def perform_action(self):
        '''Performs an action'''
        pass

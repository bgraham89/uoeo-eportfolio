#  class imports
from app.act.abstract.actuator import Actuator

#  module imports
from app.data import formats
from app.helperfunctions import converters as conv
from app.ui import tui

class Steering(Actuator):
    '''A steering wheel.'''

    def __init__(self):
        self._key = "Steering"

    def perform_action(self, data):
        '''Performs an action'''
        angle = conv.array_to_int(data[formats.ANGLE_START:formats.ANGLE_END])
        direction = data[formats.ANGLE_END]
        if angle == 180:
            information = "The car is peforming a U-Turn."
        else:
            if int(direction):
                information = "The car is taking a right."
            else:
                information = "The car is taking a left."
        tui.ux_print(information)


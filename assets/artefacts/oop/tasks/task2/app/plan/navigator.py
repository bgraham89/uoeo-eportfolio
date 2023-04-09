#  class imports
from app.plan.abstract.planner import Planner
from app.plan.models.map import Map

#  module imports
from app.data import formats
from app.helperfunctions import converters as conv

class Navigator(Planner):
    '''A component that maps the direction of the car.'''

    def __init__(self):
        self._current_orientation = None
        self._target_orientation = None
        self._instructions = []  #used as a stack
        self._key = "Navigator"
        self._directions = ("North", "East", "South", "West")
    
    def make_instruction(self, operator, operand=""):
        '''Create an instruction for the server'''
        instruction = (operator, operand)
        self._instructions.append(instruction)
    
    def request_current_orientation(self):
        '''create a request instruction for a GPS'''
        operator = "Compass"
        self.make_instruction(operator)

    def request_target_orientation(self):
        '''create a request instruction for a destination'''
        operator = "Mapper"
        self.make_instruction(operator)

    def give_instruction(self):
        '''Pop an instruction from the stack.'''
        if self._instructions:
            return self._instructions.pop()
        
    def clear_instructions(self):
        '''Clear the instruction stack.'''
        self._instructions = [] 
    
    def extract_information(self, op, data):
        '''Get useful information from data.'''
        if op == "Compass":
            self.update_current_orientation(data)
        elif op == "Mapper":
            self.update_target_orientation(data)

    def update_current_orientation(self, data):
        '''Get current location from data.'''
        num = conv.array_to_int(data)
        direction = self._directions[num]
        self._current_orientation = direction

    def update_target_orientation(self, data):
        '''Get target orientation from data.'''
        half = len(data) // 2
        current_loc = conv.array_to_int(data[:half])
        target_loc = conv.array_to_int(data[half:])
        difference = target_loc - current_loc
        if difference == 1:
            direction = "East"
        elif difference == -1:
            direction = "West"
        elif difference > 1:
            direction = "North"
        else:
            direction = "South"
        self._target_orientation = direction

    def plan(self):
        '''Formulate turning plan.'''
        if self._current_orientation and self._target_orientation:
            if self._current_orientation == self._target_orientation:
                return True
            else:
                i_curr = self._directions.index(self._current_orientation)
                i_final = self._directions.index(self._target_orientation)
                if i_curr % 2 == i_final % 2:
                    angle = conv.int_to_array(180, formats.ANGLE_END)
                    self.make_instruction("Steering", angle+["1"])
                elif i_curr + 1 % 4 == i_final:
                    angle = conv.int_to_array(90, formats.ANGLE_END)
                    self.make_instruction("Steering", angle+["1"])
                else:
                    angle = conv.int_to_array(90, formats.ANGLE_END)
                    self.make_instruction("Steering", angle+["0"])
                return True
        else:
            if not self._current_orientation:
                self.make_instruction("Compass")
            if not self._target_orientation:
                self.make_instruction("Mapper")
            return False
    




        
        
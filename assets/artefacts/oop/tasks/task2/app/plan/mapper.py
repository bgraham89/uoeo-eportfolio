from app.helperfunctions import converters
from app.plan.abstract.planner import Planner
from app.plan.models.map import Map

class Mapper(Planner):
    '''A component that maps the location of the car.'''

    def __init__(self):
        self._map = None
        self._current_location = None
        self._target_location = None
        self._plan = None
        self._instructions = []  #used as a stack
        self._key = "Mapper"
    
    def make_instruction(self, operator, operand=""):
        '''Create an instruction for the server'''
        instruction = (operator, operand)
        self._instructions.append(instruction)
    
    def request_current_location(self):
        '''create a request instruction for a GPS'''
        operator = "GPS"
        self.make_instruction(operator)

    def request_target_location(self):
        '''create a request instruction for a GPS'''
        operator = "Destination"
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
        if op == "GPS":
            self.update_current_location(data)
        elif op == "Destination":
            self.update_target_location(data)

    def update_current_location(self, data):
        '''Get current location from data'''
        num = converters.array_to_int(data)
        coords = converters.int_to_coord(num, self._map._width, self._map._height)
        self._current_location = coords

    def update_target_location(self, data):
        '''Get target location from data'''
        num = converters.array_to_int(data)
        coords = converters.int_to_coord(num, self._map._width, self._map._height)
        self._target_location = coords

    def plan(self):
        if self._current_location and self._target_location and self._map:
            start = converters.coord_to_int(self._current_location, self._map._height)
            destination = converters.coord_to_int(self._target_location, self._map._height)
            self._plan = self._map.shortest_path(start, destination)
            return True
        else:
            if not self._current_location:
                self.make_instruction("GPS")
            if not self._target_location:
                self.make_instruction("Destination")
            return False

    @classmethod
    def WithRandomMap(cls, width, height):
        '''Creates a Mapper component with randomised map.'''
        mapper = cls()
        mapper._map = Map.RandomSpanningTree(width, height)
        return mapper
    




        
        
'''Unit tests for Sensor objects'''

from context import components as avc
from context import converters as conv
import unittest

class TestMapper(unittest.TestCase):
    '''Unit tests for the Mapper class.'''

    def setUp(self):
        self.operator = "GPS"
        self.operand = 0
        self.size = 8
        self.data = conv.int_to_array(17, self.size)
    
    def test_instruction_stored(self):
        '''Expect instructiopn to be stored.'''
        mapper = avc.Mapper()
        mapper.make_instruction(self.operator, self.operand)
        self.assertTrue(mapper._instructions)

    def test_gps_request_stored(self):
        '''Expect instructiopn to be stored.'''
        mapper = avc.Mapper()
        mapper.request_current_location()
        self.assertTrue(mapper._instructions.pop()[0] == "GPS")

    def test_destination_request_stored(self):
        '''Expect instructiopn to be stored.'''
        mapper = avc.Mapper()
        mapper.request_target_location()
        self.assertTrue(mapper._instructions.pop()[0] == "Destination")

    def test_instruction_obtainable(self):
        '''Expect instructiopn to be optained.'''
        mapper = avc.Mapper()
        mapper.make_instruction(self.operator, self.operand)
        instruction = mapper.give_instruction()
        self.assertTrue(instruction)

    def test_instructions_clearable(self):
        '''Expect all instructions to be deleted.'''
        mapper = avc.Mapper()
        mapper.make_instruction(self.operator, self.operand)
        mapper.clear_instructions()
        self.assertTrue(not mapper._instructions)

    def test_random_map_assigned(self):
        '''Expect random map assigned.'''
        mapper = avc.Mapper.WithRandomMap(self.size, self.size)
        self.assertTrue(mapper._map)

    def test_current_location_assignable(self):
        '''Expect current location attribute assigned.'''
        mapper = avc.Mapper.WithRandomMap(self.size, self.size)
        mapper.extract_information("GPS", self.data)
        self.assertTrue(mapper._current_location)

    def test_target_location_assignable(self):
        '''Expect target location attribute assigned.'''
        mapper = avc.Mapper.WithRandomMap(self.size, self.size)
        mapper.extract_information("Destination", self.data)
        self.assertTrue(mapper._target_location)

    def test_plan_assignable(self):
        '''Expect random map assigned.'''
        mapper = avc.Mapper.WithRandomMap(self.size, self.size)
        mapper.extract_information("GPS", self.data)
        mapper.extract_information("Destination", self.data)
        mapper.plan()
        self.assertTrue(mapper._plan)

if __name__ == '__main__':
    unittest.main()
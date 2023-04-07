'''
Protoype class for holding data.

This class is an alternative to standard network datagram structures such as 
UDP or TPS datagrams. The purpose of the class is to provide a datastructure
to send data between components, mimicing network systems, for prototyping.
'''

from app.data.datastructures.fixedarray import FixedArray
from app.helperfunctions import encoders, guards
from app.network.config.protocols import Basic

class Package(object):
    '''An array with a seperate header and body.'''
    def __init__(self, head_size, body_size):
        guards.arg_cond((head_size,), self._size_constraints())
        guards.arg_cond((body_size,), self._size_constraints())
        self._head = FixedArray(head_size)
        self._body = FixedArray(body_size)
        self._size = head_size + body_size

    def __repr__(self):
        return f"Package(\nhead={self._head}, \nbody={self._body})"

    def __len__(self):
        return self._size

    def add_data(self, data):
        '''Add data to the Package body'''
        self._body.update(data)

    def add_meta_data(self, meta_data):
        '''Add data to the Package head'''
        self._head.update(meta_data)

    def read_data(self):
        return self._body
    
    def read_meta_data(self):
        return self._head

    def pack_meta_data(self, meta_data, tags, charlimit):
        '''
        Convert dictionary into an array, for assignment to header.
        
        tags are used as keys to get values from the meta_data 
        dictionary. values are then converted into parts of an 
        array with the charlimit as their length.
        '''
        def _slice(meta_data, tag, itemlimit):
            '''Converts meta_data value into array.'''
            return encoders.int_to_array(meta_data[tag], itemlimit)
        def _fits(meta_data, tag, itemlimit):
            '''Asserts meta_data value will fit into slice.'''
            params = (meta_data[tag],)
            condition = self._md_constraints(itemlimit)
            return guards.arg_cond(params, condition)
        def _flatten(subarrays):
            '''Unpacks nested arrays into single array'''
            return [item for subarray in subarrays for item in subarray]
        slice_generator = (_slice(meta_data, tag, charlimit) for tag in tags 
                    if _fits(meta_data, tag, charlimit))
        md_array = _flatten(slice_generator)
        return md_array
    
    def update_address(self, address):
        '''Replace the address in the header'''
        meta_data = list(self._head)
        seg = Basic.HEAD_SEGMENT_SIZE
        meta_data[seg: 2*seg] = address
        self._head.update(meta_data)

    def pad_data(self, data):
        '''Makes sure data is a suitable length'''
        while len(data) < Basic.BODY_SIZE:
            data.append("0")
        return data

    def _size_constraints(self):
        '''Assertion conditions for size of FixedArray'''
        def lower_bound(x):
            '''Checks that index isn't too small'''
            return  x >= 0
        return lambda x : lower_bound(x)
    
    def _md_constraints(self, charlimit):
        '''Assertion conditions for size of metadata values'''
        def lower_bound(x):
            '''Checks that int isn't too small'''
            return  x >= 0
        def exp_upper_bound(x, exp):
            '''Checks that int isn't too big'''
            return  x < 2 ** exp
        return lambda x : lower_bound(x) and exp_upper_bound(x, charlimit)
    
    @classmethod
    def Basic(cls, data, meta_data):
        '''
        Make a Package following a basic protocol.

        Data must be iterable, meta_data must be a dict
        with Basic tags outlined in docs.
        '''
        package = cls(Basic.HEAD_SIZE, Basic.BODY_SIZE)
        data_padded = package.pad_data(data)
        package.add_data(data_padded)
        tags = Basic.TAGS
        charlimit = Basic.HEAD_SEGMENT_SIZE
        md_array = package.pack_meta_data(meta_data, tags, charlimit)
        package.add_meta_data(md_array)
        return package

    

        

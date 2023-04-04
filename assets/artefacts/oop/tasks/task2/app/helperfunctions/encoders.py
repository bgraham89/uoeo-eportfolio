'''Helper functions for encoding data.'''

def int_to_array(number, array_size):
    '''
    Converts an int to an array of 1 and 0 strings.
    
    Any bits out of range will be discarded.
    '''
    b = bin(number)[2:]
    b_filled = b.zfill(array_size)
    b_shaped = b_filled[-array_size:]
    return  list(b_shaped)

def array_to_int(array):
    '''Converts an array of 1 and 0 strings to an int.'''
    b = "".join(array)
    return int(b, 2)

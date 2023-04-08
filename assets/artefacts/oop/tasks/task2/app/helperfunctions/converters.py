'''Helper functions for converting data.'''

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

def int_to_coord(n, w, h):
    '''
    Converts an int to Cartesian coordinates.
    
    Coordinate space is assumed to have:
    - width w,
    - height h,
    - an int id for each point
    '''
    x = n % w
    y = n // h
    return (x, y)
    
def coord_to_int(coord, h):
    '''
    Converts Cartesian Coordinates to an int.
    
    Coordinate space is assumed to have:
    - width w,
    - height h,
    - an int id for each point
    '''
    x, y = coord
    n = (y * h) + x
    return n

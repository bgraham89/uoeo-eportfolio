'''TODO: use numpy arrays instead'''

from app.helperfunctions import guards

class FixedArray(object):
    '''An array that has a fixed size.'''

    def __init__(self, size):
        self._list = [None] * size
        self._size = size

    def __repr__(self):
        return f"FixedArray({self._list})"

    def __len__(self):
        return self._size
    
    def __iter__(self):
        return (i for i in self._list)
    
    def __getitem__(self, key):
        if isinstance(key, slice):
            return [self[i] for i in range(*key.indices(self._size))]
        else:
            guards.arg_cond((key,), self._index_constraint)
            return self._list[key]
    
    def update(self, data):
        '''Replace all data'''
        guards.arg_cond((data,), self._data_constraint)
        self._list = list(data)

    def _data_constraint(self):
        '''Assertion conditions for inputting new data'''
        def length(x):
            '''Checks num indices of data matches FixedArray'''
            return self.size == len(x)
        def iterable(x):
            '''Checks data is iterable for conversion to array'''
            has_iter = hasattr(x, '__iter__')  #__iter__ then iterable
            has_getitem = hasattr(x, '__getitem__')  #alt: __getitem__ and __len__ then iterable
            return has_iter or has_getitem
        return lambda x : length(x) and iterable(x)
    
    def _index_constraints(self):
        '''Assertion conditions for indexing FixedArray'''
        def upper_bound(x):
            '''Checks that index isn't too high'''
            return  x < self._size
        def lower_bound(x):
            '''Checks that index isn't too small'''
            return  x >= 0
        return lambda x : upper_bound(x) and lower_bound(x)
        

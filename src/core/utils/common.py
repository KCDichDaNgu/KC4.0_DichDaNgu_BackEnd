from typing import List
import sys

def first_elem(iterable, default = None, condition = lambda x: True):

    try:
        return next(x for x in iterable if condition(x))
    except StopIteration:
        if default is not None and condition(default):
            return default
        else:
            raise

def first_index(iterable, default = None, condition = lambda x: True):

    try:
        return next(x for x, val in enumerate(iterable) if condition(val))
    except StopIteration:
        if default is not None and condition(default):
            return default
        else:
            raise

def convert_props_to_object(self):
    pass

def chunk_arr(input: List, size: int) -> List[List]:

    for i in range(0, len(input), size):
        yield input[i:i + size]
        
def size_of(object, unit='b'):
    
    if unit == 'b': return sys.getsizeof(object)
    elif unit == 'mb': return sys.getsizeof(object) / 1024.0**2

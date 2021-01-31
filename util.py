def manhattan_distance(pos1,pos2):
    """
    calculates the manhattan distance between two positions.
    math: |x1-x2|+|y1-y2|
    >>> pos1 = (1,2)
    >>> pos2 = (3,6)
    >>> manhattan_distance(pos1,pos2)
    6
    """
    return abs(pos1[0]-pos2[0])+abs(pos1[1]-pos2[1])

if __name__ == "__main__":
    import doctest
    doctest.testmod()

def get_random_bool(p):
    '''
    return random boolean with probability p.
    '''
    import random
    r = random.random()
    return r < p

def divide_all(dictionary,divisor):
    """
    Divides all counts of dictionary by divisor
    """
    divisor = float(divisor)
    for key in dictionary:
        dictionary[key] /= divisor
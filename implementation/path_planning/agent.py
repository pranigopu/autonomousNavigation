from basic_grid_environment import *

class Agent:
    '''A class that defines a basic unintelligent agent.'''
    
    def __init__(self, horizontal_movement_limit, vertical_movement_limit, position:list[int]=[0, 0]):
        self.position = list(position)
        self.horizontal_movement_limit = horizontal_movement_limit
        self.vertical_movement_limit = vertical_movement_limit
        self.direction_vectors = {
            'w': (1, 0),  # Up
            'a': (0, -1), # Left
            's': (-1, 0), # Down
            'd': (0, 1),  # Right
        }
        '''
        Direction vector refers to the unit vector representing a unit
        movement in a grid. In other places in this repository, this has
        also been named "focus". (p, q) means "shift by p rows and q
        columns". For now, we only consider axis-aligned movements:
        - 'w' = (1, 0)  (up)
        - 'a' = (0, -1) (left)
        - 's' = (-1, 0) (down)
        - 'd' = (0, 1)  (right)
        '''

    #================================================
    def move(self, direction_symbol:str, steps=1):
        focus = self.direction_vectors.get(direction_symbol, None)
        position = [self.position[0], self.position[1]]
        if not (focus is None):
            position[0] += focus[0] * steps
            position[1] += focus[1] * steps
        if position[0] < 0 or position[1] >= self.horizontal_movement_limit:
            return
        self.position = position
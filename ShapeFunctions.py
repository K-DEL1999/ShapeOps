import random, pygame

sides_attributes = {
    1:[1,1,1],
    2:[2,1,1],
    3:[2,2,1],
    4:[2,2,2],
    5:[3,2,2],
    6:[3,3,2],
    7:[3,3,3]
}

class entity:
    def __init__(self,shape_sides,position):
        entity.self = self
        entity.shape_sides = shape_sides
        entity.position = position

def initialize_screen_size():
    WIDTH = 700
    HEIGHT = 700
    return [WIDTH,HEIGHT]

def initialize_pygame(screen_dimensions):
    pygame.init()
    screen = pygame.display.set_mode([screen_dimensions[0],screen_dimensions[1]])
    return screen

def initialize_clock():
    clock = pygame.time.Clock()
    return clock



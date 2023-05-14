import random, pygame

def run_pygame():
    screen_dimensions = initialize_screen_size()
    screen = initialize_pygame(screen_dimensions)
    clock = initialize_clock()
    
    game_grid = [[0]*50 for i in range(50)]

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                    
        screen.fill((0,0,0))
        clock.tick(25)
        pygame.display.flip()

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

run_pygame()
pygame.quit()

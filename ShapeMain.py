import ShapeFunctions as sf

def run_pygame():
    screen_dimensions = sf.initialize_screen_size()
    screen = sf.initialize_pygame(screen_dimensions)
    clock = sf.initialize_clock()
    
    game_grid = [[0]*50 for i in range(50)]

    running = True

    while running:
        for sf.event in sf.pygame.event.get():
            if sf.event.type == sf.pygame.QUIT:
                running = False
                    
        screen.fill((0,0,0))
        clock.tick(25)
        sf.pygame.display.flip()


run_pygame()
sf.pygame.quit()



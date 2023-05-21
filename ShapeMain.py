import ShapeFunctions as sf

def run_pygame():
    screen_dimensions = sf.initialize_screen_size()
    screen = sf.initialize_pygame(screen_dimensions)
    clock = sf.initialize_clock()
    
    game_grid = [[0]*20 for i in range(20)]
    
    player = sf.player(1,1,0)
    game_grid, list_of_enemies = sf.generate_enemies(game_grid)

    printGrid(game_grid)
    
    running = True

    while running:
        for sf.event in sf.pygame.event.get():
            if sf.event.type == sf.pygame.QUIT:
                running = False
        
        game_grid, list_of_enemies = update_enemies_position(game_grid, list_of_enemies, player)            
        screen.fill((0,0,0))
        clock.tick(25)
        sf.pygame.display.flip()

def printGrid(game_grid):
    for i in range(len(game_grid)):
        for j in range(len(game_grid[0])):
            print(game_grid[i][j],end=" ")
        print()

run_pygame()
sf.pygame.quit()



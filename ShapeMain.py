import ShapeFunctions as sf

GRID_ROWS = 20
GRID_COLS = GRID_ROWS

def run_pygame():
    screen_dimensions = sf.initialize_screen_size()
    screen = sf.initialize_pygame(screen_dimensions)
    clock = sf.initialize_clock()
    
    game_grid = sf.grid([[0]*GRID_ROWS for i in range(GRID_COLS)],GRID_ROWS,GRID_COLS,screen_dimensions[0]/GRID_COLS,screen_dimensions[1]/GRID_ROWS)
    
    player = sf.player(1,1,0)
    game_grid.cells, list_of_enemies = sf.generate_enemies(game_grid.cells)

    printGrid(game_grid.cells)
    
    running = True

    while running:
        for sf.event in sf.pygame.event.get():
            if sf.event.type == sf.pygame.QUIT:
                running = False
       
        sf.display_grid(screen,game_grid.cells) 
        game_grid.cells, list_of_enemies = sf.update_enemies_position(game_grid.cells, list_of_enemies, player)            
        
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



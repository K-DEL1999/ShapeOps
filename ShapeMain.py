import ShapeFunctions as sf

GRID_ROWS = 20
GRID_COLS = GRID_ROWS

def run_pygame():
    screen_dimensions = sf.initialize_screen_size()
    screen = sf.initialize_pygame(screen_dimensions)
    clock = sf.initialize_clock()
    
    game_grid = sf.grid([[0]*GRID_ROWS for i in range(GRID_COLS)],GRID_ROWS,GRID_COLS,screen_dimensions[0]/GRID_COLS,screen_dimensions[1]/GRID_ROWS)
    
    player = sf.player(1,1,0)

    game_grid.cells = sf.place_player_on_grid(game_grid.cells,player.position//GRID_ROWS,player.position%GRID_COLS)
    game_grid.cells, list_of_enemies = sf.generate_enemies(game_grid.cells)
    for i in range(len(list_of_enemies)):
        print(list_of_enemies[i].position,end=" ")
    print()
    print(player.position)
    print("---------------------") 
    
    running = True

    while running:
        for sf.event in sf.pygame.event.get():
            if sf.event.type == sf.pygame.QUIT:
                running = False
       
        game_grid.cells, list_of_enemies = sf.update_enemies_position(game_grid.cells, list_of_enemies, player.position)            
        screen.fill((0,100,200))
        sf.display_grid(screen,game_grid) 
        clock.tick(25)
        sf.pygame.display.flip()

def printGrid(game_grid):
    for i in range(len(game_grid)):
        for j in range(len(game_grid[0])):
            print(game_grid[i][j],end=" ")
        print()

run_pygame()
sf.pygame.quit()



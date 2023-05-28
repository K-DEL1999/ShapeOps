import ShapeFunctions as sf

GRID_ROWS = 20
GRID_COLS = GRID_ROWS
UPDATE_ENEMY_POSITION_AFTER_THIS_MANY_ITERATIONS = 40

def run_pygame():
    screen_dimensions = sf.initialize_screen_size()
    screen = sf.initialize_pygame(screen_dimensions)
    clock = sf.initialize_clock()
    
    game_grid = sf.grid([[0]*GRID_ROWS for i in range(GRID_COLS)],GRID_ROWS,GRID_COLS,screen_dimensions[0]/GRID_COLS,screen_dimensions[1]/GRID_ROWS)
    
    player = sf.player(1,1,0)

    game_grid.cells = sf.place_player_on_grid(game_grid.cells,player.position//GRID_ROWS,player.position%GRID_COLS)
    game_grid.cells, list_of_enemies = sf.generate_enemies(game_grid.cells)
    
    update_enemy_position_count = 0
    game_state = 0
     
    running = True

    while running:
        for sf.event in sf.pygame.event.get():
            if sf.event.type == sf.pygame.QUIT:
                running = False
       
        if game_state == 0:
            game_state = 1
        elif game_state == 1:
            #---------------------------------------------------------------------- 
            # PLAYER MOVEMENT
            #----------------------------------------------------------------------        
            player_row = player.position//GRID_ROWS
            player_col = player.position%GRID_COLS
               
            keys = sf.pygame.key.get_pressed()
            if keys[ord('w')]: #if sf.event.key == ord('w'):                
                if player_row > 0:
                    game_grid.cells[player_row][player_col] = 0
                    game_grid.cells[player_row-1][player_col] = 1 
                    player.position = (player_row-1)*GRID_ROWS + player_col 

            elif keys[ord('a')]: #if sf.event.key == ord('a'):
                if player_col > 0:
                    game_grid.cells[player_row][player_col] = 0
                    game_grid.cells[player_row][player_col-1] = 1
                    player.position = player_row*GRID_ROWS + player_col-1

            elif keys[ord('s')]:# if sf.event.key == ord('s'):
                if player_row < GRID_ROWS-1:
                    game_grid.cells[player_row][player_col] = 0
                    game_grid.cells[player_row+1][player_col] = 1
                    player.position = (player_row+1)*GRID_ROWS + player_col
            
            elif keys[ord('d')]: #if sf.event.key == ord('d'):
                if player_col < GRID_COLS-1:
                    game_grid.cells[player_row][player_col] = 0
                    game_grid.cells[player_row][player_col+1] = 1
                    player.position = player_row*GRID_ROWS + player_col+1
            #----------------------------------------------------------------------

            if update_enemy_position_count == UPDATE_ENEMY_POSITION_AFTER_THIS_MANY_ITERATIONS:
                game_grid.cells, list_of_enemies = sf.update_enemies_position(game_grid.cells, list_of_enemies, player.position)
                update_enemy_position_count = 0
            update_enemy_position_count += 1

            screen.fill((0,100,200))
            sf.display_grid(screen,game_grid) 
        elif game_state == 2:
            screen.fill((0,100,200))
        
        clock.tick(25)
        sf.pygame.display.flip()

def printGrid(game_grid):
    for i in range(len(game_grid)):
        for j in range(len(game_grid[0])):
            print(game_grid[i][j],end=" ")
        print()

run_pygame()
sf.pygame.quit()



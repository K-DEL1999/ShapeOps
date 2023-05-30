import ShapeFunctions as sf

GRID_ROWS = 100
GRID_COLS = GRID_ROWS
FRAME_CAP = 50
UPDATE_ENEMY_POSITION_AFTER_THIS_MANY_ITERATIONS = 10
TIME_BETWEEN_EACH_SHOT = 5

def run_pygame():
    screen_dimensions = sf.initialize_screen_size()
    screen = sf.initialize_pygame(screen_dimensions)
    clock = sf.initialize_clock()
    
    game_grid = sf.grid([[0]*GRID_ROWS for i in range(GRID_COLS)],GRID_ROWS,GRID_COLS,screen_dimensions[0]/GRID_COLS,screen_dimensions[1]/GRID_ROWS)
    
    player = sf.player(1,1,0,1)
    player_projectiles = []

    game_grid.cells = sf.place_player_on_grid(game_grid.cells,player.position//GRID_ROWS,player.position%GRID_COLS)
    game_grid.cells, list_of_enemies = sf.generate_enemies(game_grid.cells)
    
    time_for_shot_count = 0
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
            if player_projectiles:
                player_projectiles, game_grid.cells = sf.update_player_projectiles(player_projectiles,game_grid.cells)
            
            player_row = player.position//GRID_ROWS
            player_col = player.position%GRID_COLS
               
            keys = sf.pygame.key.get_pressed()
            if keys[ord('w')]: #if sf.event.key == ord('w'):                
                if player_row > 0:
                    game_grid.cells[player_row][player_col] = 0
                    game_grid.cells[player_row-1][player_col] = 1 
                    player.position = (player_row-1)*GRID_ROWS + player_col
                    player.direction = 1 #up

            elif keys[ord('a')]: #if sf.event.key == ord('a'):
                if player_col > 0:
                    game_grid.cells[player_row][player_col] = 0
                    game_grid.cells[player_row][player_col-1] = 1
                    player.position = player_row*GRID_ROWS + player_col-1
                    player.direction = 2 #left
                     
            elif keys[ord('s')]:# if sf.event.key == ord('s'):
                if player_row < GRID_ROWS-1:
                    game_grid.cells[player_row][player_col] = 0
                    game_grid.cells[player_row+1][player_col] = 1
                    player.position = (player_row+1)*GRID_ROWS + player_col
                    player.direction = 3 #down
            
            elif keys[ord('d')]: #if sf.event.key == ord('d'):
                if player_col < GRID_COLS-1:
                    game_grid.cells[player_row][player_col] = 0
                    game_grid.cells[player_row][player_col+1] = 1
                    player.position = player_row*GRID_ROWS + player_col+1
                    player.direction = 4 #right
           
            # PROJECTILE MOVEMENT
            if time_for_shot_count >= TIME_BETWEEN_EACH_SHOT:
                if keys[ord(' ')]:
                    if player.direction == 1 and player_row > 1:
                        player_projectiles.append([player_row-2,player_col,player.direction])
                    elif player.direction == 3 and player_row < GRID_ROWS-2:
                        player_projectiles.append([player_row+2,player_col,player.direction])
                    elif player.direction == 2 and player_col > 1:
                        player_projectiles.append([player_row,player_col-2,player.direction])
                    elif player.direction == 4 and player_col < GRID_COLS-2:
                        player_projectiles.append([player_row,player_col+2,player.direction])
                    time_for_shot_count = 0
               
            time_for_shot_count +=1
            #----------------------------------------------------------------------

            #-----------------------------------------------------------------------------------------------------------------------
            #UPDATE ENEMY POSITION 
            #-----------------------------------------------------------------------------------------------------------------------
            if update_enemy_position_count == UPDATE_ENEMY_POSITION_AFTER_THIS_MANY_ITERATIONS:
                game_grid.cells, list_of_enemies = sf.update_enemies_position(game_grid.cells, list_of_enemies, player.position)
                update_enemy_position_count = 0
            update_enemy_position_count += 1
            #-----------------------------------------------------------------------------------------------------------------------
            
            list_of_enemies, player_projectiles, game_grid.cells = sf.enemies_projectile_collisions(list_of_enemies,player_projectiles,game_grid.cells)
            game_state = sf.check_for_collisions(player,list_of_enemies)

            screen.fill((0,100,200))
            sf.display_grid(screen,game_grid) 
        
        elif game_state == 2:
            screen.fill((0,100,200))
        
        clock.tick(FRAME_CAP)
        sf.pygame.display.flip()

def printGrid(game_grid):
    for i in range(len(game_grid)):
        for j in range(len(game_grid[0])):
            print(game_grid[i][j],end=" ")
        print()

run_pygame()
sf.pygame.quit()



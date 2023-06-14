import ShapeFunctions as sf

GRID_ROWS = 100
GRID_COLS = GRID_ROWS
SCREEN_WIDTH = 700
SCREEN_HEIGHT = SCREEN_WIDTH
CELL_WIDTH = SCREEN_WIDTH/GRID_COLS
CELL_HEIGHT = SCREEN_HEIGHT/GRID_ROWS

FRAME_CAP = 50
UPDATE_ENEMY_POSITION_AFTER_THIS_MANY_ITERATIONS = 10
TIME_BETWEEN_EACH_SHOT = 5

def run_pygame():
    screen_dimensions = sf.initialize_screen_size(SCREEN_WIDTH,SCREEN_HEIGHT)
    screen = sf.initialize_pygame(screen_dimensions)
    clock = sf.initialize_clock()
    
    game_grid = sf.grid([[0]*GRID_ROWS for i in range(GRID_COLS)],GRID_ROWS,GRID_COLS,CELL_WIDTH,CELL_HEIGHT)
    
    player = sf.player(1,5,0,1)
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
            display_shapes(screen,player,list_of_enemies)

        elif game_state == 2:
            screen.fill((0,100,200))
        
        clock.tick(FRAME_CAP)
        sf.pygame.display.flip()

def display_shapes(screen,pp,loe):
    sf.pygame.draw.polygon(screen,sf.colors[1],generate_points(pp))
    
    #for i in loe:
    #   sf.pygame.draw.polygon(screen,sf.colors[2],generate_points(i))

def generate_points(entity):
    points_A = []
    points_B = [] 
    mid_point = None
    sides = entity.shape_sides
    angle = 360 / sides
    print(angle)
    r = 1.5*CELL_WIDTH

    origin = (
        ((entity.position%GRID_COLS)*CELL_WIDTH) + CELL_WIDTH//2,
        ((entity.position//GRID_ROWS)*CELL_HEIGHT) + CELL_HEIGHT//2
    )

    if entity.direction == 1 or entity.direction == 3:
        if sides%2 == 0:
            if entity.direction == 1:
                points_A.append((origin[0],origin[1]-r))
                mid_point = (origin[0],origin[1]+r)
            else:
                points_A.append((origin[0],origin[1]+r))
                mid_point = (origin[0],origin[1]-r)
        else:
            if entity.direction == 1:
                points_A.append((origin[0],origin[1]-r))
            else:
                points_A.append((origin[0],origin[1]+r))
    elif entity.direction == 2 or entity.direction == 4:
        if sides%2 == 0:
            if entity.direction == 2:
                points_A.append((origin[0]-r,origin[1]))
                mid_point = (origin[0]+r,origin[1])
            else:
                points_A.append((origin[0]+r,origin[1]))
                mid_point = (origin[0]-r,origin[1])
        else:
            if entity.direction == 2:
                points_A.append((origin[0]-r,origin[1]))
            else:
                points_A.append((origin[0]+r,origin[1]))
         
    i = angle
    while i < 180:
        angle_a = (180 - i)/2
        angle_b = 90 - angle_a
        hyp = sf.math.sin(sf.math.radians(i))*r/sf.math.sin(sf.math.radians(angle_a))

        print("-----------------------------------------------------")
        print("i = " + str(i))
        print("angle_a = " + str(angle_a))
        print("angle_b = " + str(angle_b))
        print("hyp = " + str(hyp))

        side_A = hyp*sf.math.sin(sf.math.radians(angle_a))
        side_B = hyp*sf.math.sin(sf.math.radians(angle_b))
   
        print("side_A = " + str(side_A))
        print("side_B + " + str(side_B))
         
        start_x = points_A[0][0]
        start_y = points_A[0][1]

        if entity.direction == 1:
            new_x = start_x - side_A
            new_y = start_y + side_B
            points_A.append((new_x,new_y))
            points_B.append((start_x + side_A,new_y))
        elif entity.direction == 2:
            new_x = start_x + side_B
            new_y = start_y + side_A
            points_A.append((new_x,new_y))
            points_B.append((new_x,start_y - side_A))
        elif entity.direction == 3:
            new_x = start_x + side_A
            new_y = start_y - side_B
            points_A.append((new_x,new_y))
            points_B.append((start_x - side_A,new_y))
        elif entity.direction == 4:
            new_x = start_x - side_B
            new_y = start_y - side_A
            points_A.append((new_x,new_y))
            points_B.append((new_x,start_y + side_A))

    
        i += angle
    
        print("-----------------------------------------------------")
    
    if mid_point is not None:
        points_A.append(mid_point)

    points = points_A + points_B[::-1]

    for i in points:
        print(i)
    #exit(1)

    return points
        
def printGrid(game_grid):
    for i in range(len(game_grid)):
        for j in range(len(game_grid[0])):
            print(game_grid[i][j],end=" ")
        print()

run_pygame()
sf.pygame.quit()








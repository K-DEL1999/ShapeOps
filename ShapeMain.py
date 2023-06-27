import ShapeFunctions as sf

GRID_ROWS = 100
GRID_COLS = GRID_ROWS
SCREEN_WIDTH = 700
SCREEN_HEIGHT = SCREEN_WIDTH
GAME_INFO_BAR_HEIGHT = SCREEN_WIDTH/14
CELL_WIDTH = SCREEN_WIDTH/GRID_COLS
CELL_HEIGHT = SCREEN_HEIGHT/GRID_ROWS

FRAME_CAP = 50
UPDATE_ENEMY_POSITION_AFTER_THIS_MANY_ITERATIONS = 10
TIME_BETWEEN_EACH_SHOT = 5
ENEMY_RESPAWN_TIME = 5

text1 = "Kill Count: "
text2 = "Level: "

def run_pygame():
    screen_dimensions = sf.initialize_screen_size(SCREEN_WIDTH,(SCREEN_HEIGHT+GAME_INFO_BAR_HEIGHT))
    screen = sf.initialize_pygame(screen_dimensions)
    clock = sf.initialize_clock()
    
    #------------IN GAME TEXT-----------------
    font = sf.pygame.font.SysFont('didott.ttc',72)
    #------------ TRY AGAIN TEXT AND BUTTON -------------------
    text = initialize_end_screen(font)
    text_point = text_point_cal(text)
    try_again = initialize_try_again_text(font)
    try_again_point = try_again_point_cal(try_again,text)
    but_bound = create_button_bound(try_again,try_again_point)
    #---------------------------------------------------------

    game_grid = sf.grid([[0]*GRID_ROWS for i in range(GRID_COLS)],GRID_ROWS,GRID_COLS,CELL_WIDTH,CELL_HEIGHT)
    
    player = sf.player(1,3,0,1,0)
    player_projectiles = []

    game_grid.cells = sf.place_player_on_grid(game_grid.cells,player.position//GRID_ROWS,player.position%GRID_COLS)
    game_grid.cells, list_of_enemies = sf.generate_enemies(game_grid.cells,player.shape_sides)
    
    time_for_shot_count = 0
    update_enemy_position_count = 0
    enemy_respawn_count = 0
    game_state = 0
     
    running = True
    
    while running:
        for sf.event in sf.pygame.event.get():
            if sf.event.type == sf.pygame.QUIT:
                running = False
            if game_state == 2 and sf.event.type == sf.pygame.MOUSEBUTTONDOWN:
                mouse = sf.pygame.mouse.get_pos()
                if but_bound[0] <= mouse[0] <= but_bound[1] and but_bound[2] <= mouse[1] <= but_bound[3]:
                    player = sf.player(1,3,0,1,0)
                    player_projectiles = []
                    game_grid.cells = sf.place_player_on_grid(game_grid.cells,player.position//GRID_ROWS,player.position%GRID_COLS)
                    game_grid.cells, list_of_enemies = sf.generate_enemies(game_grid.cells,player.shape_sides)
                    time_for_shot_count = 0
                    update_enemy_position_count = 0
                    enemy_respawn_count = 0
                    game_state = 0
                    game_grid = sf.grid([[0]*GRID_ROWS for i in range(GRID_COLS)],GRID_ROWS,GRID_COLS,CELL_WIDTH,CELL_HEIGHT)

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
               
            time_for_shot_count += 1
            #----------------------------------------------------------------------

            #-----------------------------------------------------------------------------------------------------------------------
            #UPDATE ENEMY POSITION 
            #-----------------------------------------------------------------------------------------------------------------------
            if update_enemy_position_count == UPDATE_ENEMY_POSITION_AFTER_THIS_MANY_ITERATIONS:
                game_grid.cells, list_of_enemies = sf.update_enemies_position(game_grid.cells, list_of_enemies, player.position)
                update_enemy_position_count = 0
            update_enemy_position_count += 1
            #-----------------------------------------------------------------------------------------------------------------------
           
            #---------collision--------------# 
            list_of_enemies, player_projectiles, game_grid.cells, player.kill_count = sf.enemies_projectile_collisions(list_of_enemies,player_projectiles,game_grid.cells,player.kill_count)
            #--------------------------------#

            #--------Respawn Enenmies--------#
            if len(list_of_enemies) == 0:
                enemy_respawn_count += 1
            if enemy_respawn_count == ENEMY_RESPAWN_TIME:
                game_grid.cells, list_of_enemies = sf.generate_enemies(game_grid.cells,player.shape_sides)
                enemy_respawn_count = 0    
            #--------------------------------#
            
            game_state = sf.check_for_collisions(player,list_of_enemies)
            
            player.shape_sides = 3 + player.kill_count // 5

            screen.fill((0,100,200))
            sf.display_grid(screen,game_grid)
            display_shapes(screen,player,list_of_enemies)
            display_kill_count_and_level(screen,font,player)

        elif game_state == 2:
            screen.fill((0,100,200))
            screen.blit(text,text_point)
            screen.blit(try_again,try_again_point)

        clock.tick(FRAME_CAP)
        sf.pygame.display.flip()


#--------------------------- SHAPE GENERATION FUNCTIONS -----------------------------------------
def display_shapes(screen,pp,loe):
    sf.pygame.draw.polygon(screen,sf.colors[1],generate_points(pp))
    
    for i in loe:
       sf.pygame.draw.polygon(screen,sf.colors[2],generate_points(i))

def generate_points(entity):
    points_A = []
    points_B = [] 
    mid_point = None
    sides = entity.shape_sides
    angle = 360 / sides
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

        side_A = hyp*sf.math.sin(sf.math.radians(angle_a))
        side_B = hyp*sf.math.sin(sf.math.radians(angle_b))
         
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
    
    if mid_point is not None:
        points_A.append(mid_point)

    points = points_A + points_B[::-1]

    return points

#---------------------------- FUNCTION FOR KILL COUNT AND LEVEL RENDERING ----------------------------------    
def display_kill_count_and_level(screen,font,p):
    screen.blit(font.render(text1+str(p.kill_count),True,(0,0,0)),(SCREEN_WIDTH/2,SCREEN_HEIGHT))
    screen.blit(font.render(text2+str(p.shape_sides-2),True,(0,0,0)),(0,SCREEN_HEIGHT))


#---------------------------- FUNCTIONS THAT DEAL WITH TRY AGAIN PAGE ------------------------------------------
def initialize_end_screen(font):
    text = font.render('GAME OVER', True, (255,255,255))
    return text

def text_point_cal(text):
    text_x = (SCREEN_WIDTH / 2) - (text.get_rect().width / 2) 
    text_y = (SCREEN_HEIGHT / 2) - (text.get_rect().height / 2)
    
    return [text_x,text_y]
    
def initialize_try_again_text(font):
    text = font.render('Try again?', True, (255,255,255))
    return text

def try_again_point_cal(try_again,text):
    try_again_x = (SCREEN_WIDTH / 2) - (try_again.get_rect().width / 2)
    try_again_y = (SCREEN_HEIGHT / 2) - (try_again.get_rect().height / 2) + text.get_rect().height 

    return [try_again_x,try_again_y] 

def create_button_bound(try_again,try_again_point):
    width_of_bound = try_again_point[0]+try_again.get_rect().width
    height_of_bound = try_again_point[1]+try_again.get_rect().height
    return [try_again_point[0],width_of_bound,try_again_point[1],height_of_bound]

#-------------------------------------------------------------------------------------------------------------

run_pygame()
sf.pygame.quit()








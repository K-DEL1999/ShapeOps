import random as r, pygame

sides_attributes = {
    3:[1,1,1],
    4:[2,1,1],
    5:[2,2,1],
    6:[2,2,2],
    7:[3,2,2],
    8:[3,3,2],
    9:[3,3,3]
}

class entity:
    def __init__(self,ID,shape_sides,position,health):
        entity.self = self
        entity.ID = ID
        entity.shape_sides = shape_sides
        entity.position = position
        entity.health = health

class player(entity):
    def __init__(self,ID,shape_sides,position):
        super().__init__(ID,shape_sides,position)

class enemy(entity):
    def __init__(self,ID,shape_sides,position):
        super().__init__(ID,shape_sides,position)
       
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

def generate_enemies(game_grid):
    list_of_enemies = []
    row = len(game_grid)
    col = len(game_grid[0])
    
    for i in range(2,14):
        position = r.randint(0,row*col)
        while (game_grid[position//row][position%col] != 0):
            position = r.randint(0,row*col)

        game_grid[position//row][position%col] = i
        enemyInstance = enemy(i,1,position)

        list_of_enemies.append(enemyInstance)

    return game_grid, list_of_enemies

def update_enemies_position(gg,loe,p): #gg = game_grid , loe = list_of_enemies , p = player
    for i in range(len(loe)):
        enemy_row = loe[i].position//(len(gg))     #y1
        enemy_col = loe[i].position%(len(gg[0]))   #x1
        
        player_row = p[i].position//(len(gg))      #y2
        player_col = p[i].position%(len(gg[0]))    #x2

        #TODO ----------------------
        # Breaks if x2=x1
        # 
        #----------------------------

        m = get_slope(player_col)
        b = get_intercept(m,enemy_row,enemy_col)

        if enemy_col < player_col:
            new_enemy_col = enemy_col + 1
            new_enemy_row = m*(new_enemy_col) + b
            gg[new_enemy_row][new_enemy_col] = loe.ID
            loe.position = (new_enemy_row*len(gg)) + new_enemy_col
        else if enemy_col > player_col:
            new_enemy_col = enemy_col - 1
            new_enemy_row = m*(new_enemy_col) + b
            gg[new_enemy_row][new_enemy_col] = loe.ID
            loe.position = (new_enemy_row*len(gg)) + new_enemy_col
        else:
            if enemy_row < player_row:
                new_enemy_row = enemy_row + 1
                gg[new_enemy_row][enemy_col] = loe.ID
                loe.position = (new_enemy_row*len(gg)) + enemy_col    
            else if enemy_row > player_row:
                new_enemy_row = enemy_row - 1
                gg[new_enemy_row][enemy_col] = loe.ID
                loe.position = (new_enemy_row*len(gg)) + enemy_col 
            else:
                pass           

    return gg,loe

def get_slope(y2,y1,x2,x1):
    return (y2-y1)/(x2-x1)

def get_intercept(m,y1,x1):
    return y1-(m*x1)
    

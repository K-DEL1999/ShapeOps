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
    def __init__(self,ID,shape_sides,position):
        entity.self = self
        entity.ID = ID
        entity.shape_sides = shape_sides
        entity.position = position

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
    player_row = p.position//(len(gg))      #y2
    player_col = p.position%(len(gg[0]))    #x2

    for i in range(len(loe)):
        enemy_row = loe[i].position//(len(gg))     #y1
        enemy_col = loe[i].position%(len(gg[0]))   #x1
        
        gg,loe = get_new_position(gg,loe,player_row,player_col,enemy_row,enemy_col) 

    return gg,loe

def get_new_position(gg,loe,y2,x2,y1,x1):
    if x2 == x1:
        if y1 < y2:
            new_y1 = y1 + 1
            gg[new_y1][x1] = loe.ID
            loe.position = (new_y1*len(gg)) + x1    
        elif y1 > y2:
            new_y1 = y1 - 1
            gg[new_y1][x1] = loe.ID
            loe.position = (new_y1*len(gg)) + x1 
        else:
            pass 
    else:
        m = get_slope(x2)
        b = get_intercept(m,y1,x1)

        if x1 < x2:
            new_x1 = x1 + 1
        elif x1 > x2:
            new_x1 = x1 - 1
        
        new_y1 = m*(new_x1) + b
        gg[new_y1][new_x1] = loe.ID
        loe.position = (new_y1*len(gg)) + new_x1

    return gg,loe

def get_slope(y2,y1,x2,x1):
    return (y2-y1)/(x2-x1)

def get_intercept(m,y1,x1):
    return y1-(m*x1)
    

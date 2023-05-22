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

class grid:
    def __init__(self,cells,rows,cols,cell_width,cell_height):
        grid.self = self
        grid.cells = cells
        grid.rows = rows
        grid.cols = cols
        grid.cell_width = cell_width
        grid.cell_height = cell_height

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

def display_grid(screen,gg):
    pass

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
        
        new_enemy_row, new_enemy_col = get_new_position(player_row,player_col,enemy_row,enemy_col) 

        gg[new_enemy_row][new_enemy_col] = loe[i].ID
        loe[i].position = (new_enemy_row*len(gg)) + new_enemy_col

    return gg,loe


def get_new_position(y2,x2,y1,x1): #Destination ---> (y2,x2) // start point ---> (y1,x1)
    new_x1 = x1
    new_y1 = y1

    if x2 == x1 and y2 == y1:
        pass
    elif x2 == x1:
        if y2 < y1:
            new_y1 -= 1
        else:
            new_y1 += 1      
    elif y2 == y1:
        if x2 < x1:
            new_x1 -= 1
        else:
            new_x1 += 1
    else:
        if y2 > y1:
            new_y1 += 1
        else:
            new_y1 -= 1
        if x2 < x1:
            new_x1 -= 1
        else:
            new_x1 += 1

    return new_y1, new_x1


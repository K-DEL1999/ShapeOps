import random as r, pygame, math

ENEMY_COUNT = 40

sides_attributes = {
    3:[1,1,1],
    4:[2,1,1],
    5:[2,2,1],
    6:[2,2,2],
    7:[3,2,2],
    8:[3,3,2],
    9:[3,3,3]
}

colors = {
    0:(0,0,0),
    1:(255,255,255),
    2:(0,255,0),
    3:(0,255,255)
}

class grid:
    def __init__(self,cells,rows,cols,cell_width,cell_height):
        self.cells = cells
        self.rows = rows
        self.cols = cols
        self.cell_width = cell_width
        self.cell_height = cell_height

class entity:
    def __init__(self,ID,shape_sides,position,direction):
        self.ID = ID
        self.shape_sides = shape_sides
        self.position = position
        self.direction = direction

class player(entity):
    def __init__(self,ID,shape_sides,position,direction,kill_count):
        super().__init__(ID,shape_sides,position,direction)
        self.kill_count = kill_count

class enemy(entity):
    def __init__(self,ID,shape_sides,position,direction):
        super().__init__(ID,shape_sides,position,direction)
       
def initialize_screen_size(W,H):
    WIDTH = W
    HEIGHT = H
    return [WIDTH,HEIGHT]

def initialize_pygame(screen_dimensions):
    pygame.init()
    screen = pygame.display.set_mode([screen_dimensions[0],screen_dimensions[1]])
    return screen

def initialize_clock():
    clock = pygame.time.Clock()
    return clock

def display_grid(screen,gg):
    rows = gg.rows
    cols = gg.cols

    cell_width = gg.cell_width
    cell_height =gg.cell_height

    x_coord = 0
    y_coord = 0

    for i in range(rows):
        for j in range(cols):
            if gg.cells[i][j] == 0:
                pygame.draw.rect(screen,colors[0],pygame.Rect(x_coord,y_coord,cell_width,cell_height)) 
            elif gg.cells[i][j] == -1:
                pygame.draw.circle(screen,colors[3],(x_coord+(cell_width//2),y_coord+(cell_height//2)),cell_width//2,0)
            elif gg.cells[i][j] == 1:
                pygame.draw.rect(screen,colors[1],pygame.Rect(x_coord,y_coord,cell_width,cell_height)) 
            else:
                pygame.draw.rect(screen,colors[2],pygame.Rect(x_coord,y_coord,cell_width,cell_height))
            x_coord += cell_width
        
        x_coord = 0
        y_coord += cell_height

def place_player_on_grid(gg,row,col):
    gg[row][col] = 1
    return gg
    
def generate_enemies(game_grid,ps):
    list_of_enemies = []
    row = len(game_grid)
    col = len(game_grid[0])
    
    for i in range(2,ENEMY_COUNT+2):
        enemy_position = r.randint(0,(row*col)-1)
        while (game_grid[enemy_position//row][enemy_position%col] != 0):
            enemy_position = r.randint(0,row*col)

        game_grid[enemy_position//row][enemy_position%col] = i

        list_of_enemies.append(enemy(i,r.randint(3,ps+1),enemy_position,1))
   
    return game_grid, list_of_enemies

def update_player_projectiles(pp,gg):
    new_pp = []
    rows = len(gg)
    cols = len(gg[0])

    for i in range(len(pp)):
        gg[pp[i][0]][pp[i][1]] = 0

        if pp[i][2] == 1:
            if pp[i][0] > 0:
                pp[i][0] -= 1
                new_pp.append(pp[i])
                gg[pp[i][0]][pp[i][1]] = -1 
                
        elif pp[i][2] == 2:
            if pp[i][1] > 0:
                pp[i][1] -= 1
                new_pp.append(pp[i])
                gg[pp[i][0]][pp[i][1]] = -1 

        elif pp[i][2] == 3:
            if pp[i][0] < rows-1:
                pp[i][0] += 1
                new_pp.append(pp[i])
                gg[pp[i][0]][pp[i][1]] = -1 

        elif pp[i][2] == 4:
            if pp[i][1] < cols-1:
                pp[i][1] += 1 
                new_pp.append(pp[i])
                gg[pp[i][0]][pp[i][1]] = -1 
        
    return new_pp, gg 


def update_enemies_position(gg,loe,p): #gg = game_grid , loe = list_of_enemies , p = player
    player_row = p//(len(gg))      #y2
    player_col = p%(len(gg[0]))    #x2

    for i in range(len(loe)):
        enemy_row = loe[i].position//(len(gg))     #y1
        enemy_col = loe[i].position%(len(gg[0]))   #x1

        new_enemy_row, new_enemy_col = get_new_position(player_row,player_col,enemy_row,enemy_col) 
        if gg[new_enemy_row][new_enemy_col] not in range(2,ENEMY_COUNT+2):
            gg[enemy_row][enemy_col] = 0 
            gg[new_enemy_row][new_enemy_col] = loe[i].ID
            loe[i].position = (new_enemy_row*len(gg)) + new_enemy_col
            
            if enemy_row > new_enemy_row: # up
                loe[i].direction = 1
            elif enemy_row < new_enemy_row: # down 
                loe[i].direction = 3
            elif enemy_col > new_enemy_col: # left
                loe[i].direction = 2
            elif enemy_col < new_enemy_col: # right
                loe[i].direction = 4
        
    return gg,loe

def get_new_position(y2,x2,y1,x1): #Destination ---> (y2,x2) // start point ---> (y1,x1)
    new_x1 = x1
    new_y1 = y1

    if x2 == x1:
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

def check_for_collisions(p,loe):
    for i in range(len(loe)):
        if p.position == loe[i].position:
            return 2    
    return 1

def enemies_projectile_collisions(loe,pp,gg,kc):
    new_loe = []
    new_pp = []
    used_projectiles = []
    
    for i in range(len(loe)):
        collision = 0
        enemy_row = loe[i].position//len(gg)
        enemy_col = loe[i].position%len(gg[0])

        for j in range(len(pp)):
            if enemy_row == pp[j][0] and enemy_col == pp[j][1]:
                collision = 1
                gg[enemy_row][enemy_col] = 0
                used_projectiles.append(j)
                kc += 1
                break;

        if not collision:
            new_loe.append(loe[i])

    for i in range(len(pp)):
        if i not in used_projectiles:
            new_pp.append(pp[i])

    return new_loe, new_pp, gg, kc




 










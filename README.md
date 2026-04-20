# ShapeOps

ShapeOps is a game inspired by love of mathemtics and my love of zombies. The premise of the game is to kill as many zombie shapes as you can and as you reach a certain certain threshold of kills you evolve. You start of as a triangle and with each evolution you gain an extra side. This goes on indefinitely until you eventually fall to the never ending hoard of zombie shapes. This game was developed with the pygames library provided by python3 and was written entirely in python.I hope one day to convert this game to C and flash onto a microcontroller so it can be played on a self made handle held gaming device.

# Project Structure

- **ShapeFunctions.py**: contains function definitions
- **ShapeMain.py**: contains main driving code for game

# Layout Of Code

## Initialization

The main code begins by defining variables that will set the boundaries of the window that will run the game. 

```python
GRID_ROWS = 100
GRID_COLS = GRID_ROWS
SCREEN_WIDTH = 700
SCREEN_HEIGHT = SCREEN_WIDTH
GAME_INFO_BAR_HEIGHT = SCREEN_WIDTH/14
CELL_WIDTH = SCREEN_WIDTH/GRID_COLS
CELL_HEIGHT = SCREEN_HEIGHT/GRID_ROWS
```

These values are used in the intialization found in the beginning of the main function.

```python
def run_pygame():
    screen_dimensions = sf.initialize_screen_size(SCREEN_WIDTH,(SCREEN_HEIGHT+GAME_INFO_BAR_HEIGHT))
    screen = sf.initialize_pygame(screen_dimensions)
    clock = sf.initialize_clock()
.
.
.
```

Following the screen initialization is the grid initialization and setting the starting state of other variables. The grid enables allows the prorgam to keep track of everything on the screen.

```python
.
.
.
    game_grid = sf.grid([[0]*GRID_ROWS for i in range(GRID_COLS)],GRID_ROWS,GRID_COLS,CELL_WIDTH,CELL_HEIGHT)
    
    player = sf.player(1,3,0,1,0)
    player_projectiles = []

    game_grid.cells = sf.place_player_on_grid(game_grid.cells,player.position//GRID_ROWS,player.position%GRID_COLS)
    game_grid.cells, list_of_enemies = sf.generate_enemies(game_grid.cells,player.shape_sides)
    
    time_for_shot_count = 0
    update_enemy_position_count = 0
    enemy_respawn_count = 0
    game_state = 0

.
.
.
```

## Game Loop

Once the screen and grid are rady we can begin rendering by entering an infinite loop.

```python
.
.
.
    while running:
        .
        .
        .
.
.
.
```

The game loop is broken up into multiple sections - **updating player position**, **udpating projectile position**, **updating enemy position**, **possible collisions** and **Respawning Enemies**

### Updating player position

We keep track of the players position by assigning them a coordinate from the grid. Depending on whether 'w', 'a', 's', or 'd' the position is updated accordingly. The new position us updated with a 1 while the old position is set to 0.

```python
.
.
.           
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
.
.
.
    
```

### Updating projectile position

Projectiles are kept track of in the `player_projectiles` list. Everytime a new one is created it is appended to the list. Updating the projectiles position is easy since they only move in one direction. The direction is based on the players direction at the time of firing.

```python
.
.
.
            if player_projectiles:
                player_projectiles, game_grid.cells = sf.update_player_projectiles(player_projectiles,game_grid.cells)
.
.
.
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
.
.
.
```

### Updating enemy position

Enemies always want to move closer to the enemy so we update their position based on the position of the player. The same idea applies to enemies as with players, new location becomes enemy number while old location is set to 0.

```python
.
.
.
            if update_enemy_position_count == UPDATE_ENEMY_POSITION_AFTER_THIS_MANY_ITERATIONS:
                game_grid.cells, list_of_enemies = sf.update_enemies_position(game_grid.cells, list_of_enemies, player.position)
                update_enemy_position_count = 0
            update_enemy_position_count += 1
.
.
.
```

### Possible collisions 

A check is done with the list of all enemies and list of all projectiles to see if any groups shares a similar location. 

```python
.
.
.
            list_of_enemies, player_projectiles, game_grid.cells, player.kill_count = sf.enemies_projectile_collisions(list_of_enemies,player_projectiles,game_grid.cells,player.kill_count)
.
.
.
```

This is the definition for the collision function.

```python
.
.
.
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
.
.
.
```

The play collision is done in a different function. The function checks if an enemy and player have the same location on the grid. Player however is not effected by their own projectiles. This collision is seperated because it changes the state of the game - from running to terminating.

```python
    game_state = sf.check_for_collisions(player,list_of_enemies)
```

This is the definition

```python
def check_for_collisions(p,loe):
    for i in range(len(loe)):
        if p.position == loe[i].position:
            return 2    
    return 1
```

### Respawning Enemies

This just makes sure that there are an appropriate number of enemies on the grid. It only spawns them after you have killed an entire wave.

```python
            if len(list_of_enemies) == 0:
                enemy_respawn_count += 1
            if enemy_respawn_count == ENEMY_RESPAWN_TIME:
                game_grid.cells, list_of_enemies = sf.generate_enemies(game_grid.cells,player.shape_sides)
                enemy_respawn_count = 0    
```

## Displaying Updates

Finally after all the updates to the grid and other status variables the changes are reflected on the small window display

```python
            screen.fill((0,100,200))
            sf.display_grid(screen,game_grid)
            display_shapes(screen,player,list_of_enemies)
            display_kill_count_and_level(screen,font,player)
```

## How To Run

**ensure your device has python3 installed and has the pygames library downloaded**

1. Clone repository
2. Change to ShapeOps directory
3. run `python3 ShapeMain.py`
4. Enjoy !







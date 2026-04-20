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

# 

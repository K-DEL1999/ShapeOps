# ShapeOps

ShapeOps is a game inspired by love of mathemtics and my love of zombies. The premise of the game is to kill as many zombie shapes as you can and as you reach a certain certain threshold of kills you evolve. You start of as a triangle and with each evolution you gain an extra side. This goes on indefinitely until you eventually fall to the never ending hoard of zombie shapes. This game was developed with the pygames library provided by python3 and was written entirely in python.I hope one day to convert this game to C and flash onto a microcontroller so it can be played on a self made handle held gaming device.

# Project Structure

- **ShapeFunctions.py**: contains function definitions
- **ShapeMain.py**: contains main driving code for game

# Layout Of Code

The main code begins by defining variables that will set the boundaries of the window that will run the game

```python
GRID_ROWS = 100
GRID_COLS = GRID_ROWS
SCREEN_WIDTH = 700
SCREEN_HEIGHT = SCREEN_WIDTH
GAME_INFO_BAR_HEIGHT = SCREEN_WIDTH/14
CELL_WIDTH = SCREEN_WIDTH/GRID_COLS
CELL_HEIGHT = SCREEN_HEIGHT/GRID_ROWS
```

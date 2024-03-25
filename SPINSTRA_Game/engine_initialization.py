from Engine import CEngine
from constants import GAME_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT, GAME_FPS

# Initialize a Game Engine object with the title of our game
GameEngine = CEngine(GAME_TITLE)

# Use the Game Engine to initialize a Pygame window with the specified dimensions and FPS
GameEngine.initializePygame(SCREEN_WIDTH, SCREEN_HEIGHT, GAME_FPS)
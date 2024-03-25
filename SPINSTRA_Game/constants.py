# Game window options
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
GAME_FPS = 60
GAME_TITLE = "SPINSTRA Python Game"
WINDOW_CLEAR_COLOR = (0, 0, 0, 0)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHT_GREEN = (50, 168, 82)
BLUE = (0, 0, 255)
LIGHT_BLUE = (59, 91, 235)
MAP_BACKGROUND = (0, 26, 26)
HALLWAY_COLOR = (77, 77, 0)
ROOM_COLOR = (255, 0, 0)
CURRENT_ROOM_COLOR = (255, 255, 25)
BATTLE_OPTIONS_BACKGROUND_COLOR = (0, 26, 51)
BATTLE_TEXT_HIGHLIGHT_COLOR = (255, 255, 153)

# Map
MAP_SIZE = 450

# Font Info
GAME_FONT_PATH = "Assets/Fonts/Terminess.ttf"

# Font Sizes
XXS_FONT_SIZE = 2
XS_FONT_SIZE = 5
SM_FONT_SIZE = 12
REG_FONT_SIZE = 20
MED_FONT_SIZE = 30
TITLE_FONT_SIZE = 40

# Menu Configurations
MAIN_MENU = {
    "title": GAME_TITLE,
    "options": ["New Game", "Continue", "Scoreboard", "Exit"]
}

PAUSE_MENU = {
    "title": "PAUSE",
    "options": ["Resume", "View Stats", "Edit Review Topics", "Exit Without Saving", "Save and Quit"]
}

# Battle Info
REGULAR_ENEMY_BASE_HEALTH = 10
BOSS_ENEMY_BASE_HEALTH = 20

# Filepaths (relative to main.py)
QUESTIONS_DIRPATH = "Data/Questions"
LEVELS_FILEPATH = "Data/levels.json"
CHARACTER_TYPES_FILEPATH = "Data/characters.json"
ENEMY_TYPES_FILEPATH = "Data/enemies.json"
BOSS_TYPES_FILEPATH = "Data/bosses.json"
ITEM_TYPES_FILEPATH = "Data/items.json"
MAP_ICONS_INFO_FILEPATH = "Data/map_icons.json"
TREASURE_CHEST_ICON_FILEPATH = "Assets/Misc/Treasure_Chest/chests.png"
SCOREBOARD_FILEPATH = "Engine/scoreboard.csv"

# Level Data
LEVEL_TYPES = ["Battle", "Treasure", "Mystery"]

# Difficulties
EASY_DIFFICULTY = 0
MEDIUM_DIFFICULTY = 1
HARD_DIFFICULTY = 2
EXTRA_HARD_DIFFICULTY = 3

# Starting items for the user
STARTING_ITEMS = ["Potion", "Bomb", "Tonic", "Elixir"]

# "Super Secret" Encryption Info
RSA_PUBLIC_KEY = 2917303
RSA_PRIVATE_KEY = 1819399
RSA_PRIMES_PRODUCT = 9427657
CIPHER_SEPARATOR = "///"

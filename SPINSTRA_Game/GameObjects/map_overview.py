from .game_object import GameObject
from .level_map import LevelMap
from .inventory_display import InventoryDisplay
from .interactive_rect import InteractiveRect
from .animated_sprite import AnimatedSprite
from .simple_text import SimpleText
from .healthbar import HealthBar
from .battle_info_window import BattleInfoWindow
from GameOperation import LevelLoader
from constants import *
import pygame

# Class that implements the Map Overview
class MapOverview(GameObject):
    #------------------------------#
    # Constructor Function
    def __init__(self, parentID="", newGame=False, hidden=False):
        super().__init__()
        self.character = self.getGlobalDictValue("character")
        self.parentID = parentID
        self.hidden = False
        self.levelLoader = None
        self.characterHealthBar = None
        self.characterNameLabel = None
        self.infoWindow = None

        # If it's a new game
        if newGame:
            # Intialize the level loader
            self.levelLoader = LevelLoader()

            # Load the levels
            if (not self.levelLoader.loadLevels()):
                print('Dude - something went horribly wrong. There are no levels in the levels.json file!!!')

            # Get the formatted current level data and put it in the game engine's global dict
            currentLevelData = self.levelLoader.getCurrentLevelData()
            self.setGlobalDictValue("currentLevelData", currentLevelData)
            self.currentLevelData = currentLevelData

            # Get the user's current location
            currentLevelData["currentLocation"] = self.levelLoader.getCurrentLocation()

            # Give the player some default items in their inventory
            items = self.getGlobalDictValue("items")
            for item in items:
                if item["name"] in STARTING_ITEMS:
                    self.character["inventory"].append(item)
        else:
            # If it's a loaded game, simply get the current level data from the game engine's global dict
            self.currentLevelData = self.getGlobalDictValue("currentLevelData")

        # Initialize the map overview UI elements
        self.mapOverviewElements = []
        self.initializeMapOverviewElements()
        
        # Save the game
        self.saveGame()
    #------------------------------#

    #------------------------------#
    # Function that initializes elements used in the map overview screens
    def initializeMapOverviewElements(self):
        # Show the map and set a signal listener
        levelMap = LevelMap(parentID=self.gameObjectID, zIndex=1)
        self.mapOverviewElements.append({"name": "map", "level-map": levelMap})
        self.setSignalListener(msg="move-to-room", sourceID=levelMap.getGameObjectID(), callback=self.moveToRoom)

        # Initialize the level title
        levelTitleText = self.currentLevelData["name"]
        levelTitleWidth, levelTitleHeight = pygame.font.Font(GAME_FONT_PATH, TITLE_FONT_SIZE).size(levelTitleText)
        levelTitleTLx = SCREEN_WIDTH//2 - levelTitleWidth//2
        levelTitleTLy = 240 - 15 - levelTitleHeight
        levelTitle = SimpleText(text=levelTitleText, fontSize=TITLE_FONT_SIZE, x=levelTitleTLx, y=levelTitleTLy)
        self.mapOverviewElements.append({"name": "level-title", "text": levelTitle})

        # Show the character's health
        self.characterHealthBar = HealthBar(TLx=7, TLy=SCREEN_HEIGHT//2 + 200, maxHealth=self.character["maxHealth"], initialHealth=self.character["HP"])

        # Show the character's name
        characterNameWidth, _ = pygame.font.Font(GAME_FONT_PATH, MED_FONT_SIZE).size(self.character["name"])
        self.characterNameLabel = SimpleText(text=self.character["name"], fontSize=MED_FONT_SIZE, x=200-characterNameWidth//2, y=SCREEN_HEIGHT//2 - 200)

        # Show the character
        characterSprite = AnimatedSprite("Assets", self.character["type"]["animations"], scaleFactor=4, centerX=200, centerY=SCREEN_HEIGHT//2)
        self.mapOverviewElements.append({"name": "character", "sprite": characterSprite})

        # Show the user's inventory
        inventoryDisplay = InventoryDisplay(parentID=self.gameObjectID)
        self.mapOverviewElements.append({"name": "inventory-display", "inventory-display": inventoryDisplay})
        self.setSignalListener(msg="item-used", sourceID=inventoryDisplay.getGameObjectID(), callback=self.itemUsed)

        # Initialize the "Enter" button and set a signal listener
        enterTextWidth, enterTextHeight = pygame.font.Font(GAME_FONT_PATH, MED_FONT_SIZE).size("Enter")
        enterButtonTLx = SCREEN_WIDTH//2-enterTextWidth//2
        enterButtonTLy = SCREEN_HEIGHT-160
        enterButton = InteractiveRect(enterButtonTLx, enterButtonTLy, width=enterTextWidth, height=enterTextHeight, text="Enter", textCoordinates=(enterButtonTLx, enterButtonTLy), defaultColor=BLACK, highlightColor=WHITE, defaultTextColor=WHITE, highlightTextColor=BLACK, fontSize=MED_FONT_SIZE, callbackArg=None, parentID=self.gameObjectID)
        enterButtonID = enterButton.getGameObjectID()
        self.setSignalListener(msg="clicked", sourceID=enterButtonID, callback=self.enterButtonPressed)

        self.mapOverviewElements.append({"name": "enter-button", "rect": enterButton})
    #------------------------------#

    #------------------------------#
    # Function that is called when the enter button is pressed
    def enterButtonPressed(self, _):
        currentLevelData = self.getGlobalDictValue("currentLevelData")
        currentLocation = currentLevelData["currentLocation"]

        roomData = {}

        for room in currentLevelData["roomData"]:
            coordinates = (room["coordinates"][0], room["coordinates"][1])
            if coordinates == currentLocation and (not room["completed"]):
                # Don't let the user enter the boss room unless they have the Boss Key in their inventory
                if room["type"] == "Boss":
                    self.character = self.getGlobalDictValue("character")
                    inventory = self.character["inventory"]

                    bossKeyFound = False
                    for item in inventory:
                        if item["name"] == "Boss Key":
                            roomData = room
                            self.emitSignal(msg="room-entered", data=roomData, targetID=self.parentID)
                            bossKeyFound = True
                            break

                    if not bossKeyFound:
                        self.infoWindow = BattleInfoWindow("You need to find the Boss Key!", parentID=self.gameObjectID)
                        self.setSignalListener(msg="close", sourceID=self.infoWindow.getGameObjectID(), callback=self.closeInfoWindow)
                            
                # If it's a normal room, let the user enter
                else:
                    roomData = room
                    self.emitSignal(msg="room-entered", data=roomData, targetID=self.parentID)
                    break
    #------------------------------#

    #------------------------------#
    # Function that hides the map overview
    def hide(self):
        for el in self.mapOverviewElements:
            if el["name"] == "map":
                el["level-map"].__del__()
            elif el["name"] == "character":
                el["sprite"].__del__()
            elif el["name"] == "inventory-display":
                el["inventory-display"].__del__()
            elif el["name"] == "enter-button":
                el["rect"].__del__()
            elif el["name"] == "level-title":
                el["text"].__del__()
            else:
                pass

        if (self.characterHealthBar != None):
            self.characterHealthBar.__del__()

        if (self.characterNameLabel != None):
            self.characterNameLabel.__del__()

        if (self.infoWindow != None):
            self.infoWindow.__del__()
    #------------------------------#

    #------------------------------#
    # Function that shows the map overview
    def show(self):
        self.initializeMapOverviewElements()
    #------------------------------#

    #------------------------------#
    # Function that is called when a user clicks a valid room on the map to move to
    def moveToRoom(self, roomCoordinates):
        currentLevelData = self.getGlobalDictValue("currentLevelData")
        currentLevelData["currentLocation"] = roomCoordinates

        # Honestly this is pretty terrible, but it's too late in the development process to fix it - sorry!
        # It literally just deletes and recreates everything again to handle updating the level map
        self.hide()
        self.show()
    #------------------------------#

    #------------------------------#
    # Function that loads the next level if one exists  
    def goToNextLevel(self):
        # Calculate the new level index
        currentLevelData = self.getGlobalDictValue("currentLevelData")
        currentLevelIndex = currentLevelData["levelIndex"]
        newLevelIndex = currentLevelIndex + 1

        # Reset the level loader object with the newLevelIndex, if it exists
        if (self.levelLoader != None):
            self.levelLoader.__del__()
        
        self.levelLoader = LevelLoader(currentLevelIndex=newLevelIndex)
        
        # If there are no more levels to load, emit the "game-finished" signal
        if (not self.levelLoader.loadLevels()):
            self.emitSignal(msg="game-finished", data=None, targetID=self.parentID)
            return
        
        # Hide the map overview
        self.hide()
        
        # Load in the new level data
        currentLevelData = self.levelLoader.getCurrentLevelData()
        self.setGlobalDictValue("currentLevelData", currentLevelData)
        self.currentLevelData = currentLevelData
        currentLevelData["currentLocation"] = self.levelLoader.getCurrentLocation()

        # Increment the user's max health by 10 since they just completed a level
        character = self.getGlobalDictValue("character")
        character["maxHealth"] += 10
        character["HP"] = character["maxHealth"]

        # Remove the previous level's boss key from the user's inventory
        for item in character["inventory"]:
            if (item["name"] == "Boss Key"):
                character["inventory"].remove(item)
                break

        # Show the map overview again
        self.show()
    #------------------------------#

    #------------------------------#
    # Function that is called whenever the user uses an item from their inventory   
    def itemUsed(self, _):
        # Update the character's health bar with the current health value
        self.characterHealthBar.updateHealthValue(self.character["HP"])
    #------------------------------#

    #------------------------------#
    # Function that is called to close the info window   
    def closeInfoWindow(self, _):
        self.removeSignalListenerBySourceID(self.infoWindow.getGameObjectID())
        self.infoWindow.__del__()
    #------------------------------#
from constants import *
from utils import loadJSONFile
from .room_loader import RoomLoader

# Class that implements a Level Loader
class LevelLoader:
    #------------------------------#
    # Constructor Function
    def __init__(self, currentLevelIndex=0, currentRoomLocation=None):
        self.levels = []
        self.currentLevel = None
        self.currentLevelIndex = currentLevelIndex
        self.currentRoomLocation = currentRoomLocation
    #------------------------------#

    #------------------------------#
    # Destructor Function
    def __del__(self):
        self.levels = []
    #------------------------------#

    #------------------------------#
    # Function that loads the levels from the JSON file at LEVELS_FILEPATH
    def loadLevels(self):
        self.levels = loadJSONFile(LEVELS_FILEPATH)

        if (self.currentLevelIndex > len(self.levels) - 1):
            return False
        
        self.currentLevel = self.levels[self.currentLevelIndex]
        if self.currentRoomLocation == None:
            self.currentRoomLocation = (self.currentLevel["entryCoordinates"][0], self.currentLevel["entryCoordinates"][1])

        return True
    #------------------------------#

    #------------------------------#
    # Function that progresses to the next level
    def progressToNextLevel(self):
        self.currentLevelIndex += 1
        self.loadLevels()
    #------------------------------#

    #------------------------------#
    # Function that returns an array of coordinates of all rooms in the current level map
    def getRoomsInCurrentLevel(self):
        rooms = []

        for rowIndex, row in enumerate(self.currentLevel["map"]):
            for colIndex, col in enumerate(row):
                if col == "r":
                    rooms.append([rowIndex, colIndex])

        return rooms
    #------------------------------#

    #------------------------------#
    # Function that randomly determines the types of level rooms (with exception of the exit room, which is always a Boss Room)
    def generateLevelRoomTypes(self):
        rooms = self.getRoomsInCurrentLevel()
        typedRooms = RoomLoader.generateRoomTypes(rooms, self.currentLevel["exitCoordinates"])
        return typedRooms
    #------------------------------#

    #------------------------------#
    # Function that returns the current level map
    def getCurrentLevelMap(self):
        return self.currentLevel["map"]
    #------------------------------#

    #------------------------------#
    # Function that returns the info for the current room
    def getCurrentRoom(self):
        return self.roomLoader.generateRoom(self.currentRoomLocation == self.currentLevel["exitCoordinates"])
    #------------------------------#

    #------------------------------#
    # Function that formats and returns the current level data
    def getCurrentLevelData(self):
        self.currentLevel = self.levels[self.currentLevelIndex]
        currentLevelData = {}
        currentLevelData["map"]  = self.currentLevel["map"]
        currentLevelData["roomData"] = self.generateLevelRoomTypes()
        currentLevelData["name"] = self.currentLevel["name"]
        currentLevelData["levelIndex"] = self.currentLevelIndex
        currentLevelData["maxDifficulty"] = int(self.currentLevel["maxDifficulty"])
        return currentLevelData
    #------------------------------#

    #------------------------------#
    # Function that returns the coordinates of the user's location in the current level
    def getCurrentLocation(self):
        return self.currentRoomLocation
    #------------------------------#
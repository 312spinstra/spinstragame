import pygame
from .game_object import GameObject
from .interactive_rect import InteractiveRect
from .icon import Icon
from constants import *
from utils import loadJSONFile

# Class that implements the Level Map
class LevelMap(GameObject):
    #------------------------------#
    # Constructor Function
    def __init__(self, centerX=SCREEN_WIDTH//2, centerY=SCREEN_HEIGHT//2, parentID="", zIndex=0):
        super().__init__(zIndex=zIndex)
        self.parentID = parentID
        self.currentLevelData = self.getGlobalDictValue("currentLevelData")
        self.map = self.currentLevelData["map"]
        self.roomData = self.currentLevelData["roomData"]
        self.currentLocation = self.currentLevelData["currentLocation"]
        self.centerX = centerX
        self.centerY = centerY
        self.icons = {}
        self.roomRects = []
        self.roomIconInfo = []
        self.roomIcons = []
        self.mapIconInfo = loadJSONFile(MAP_ICONS_INFO_FILEPATH)

        self.possibleRooms = []

        self.processedNodes = []
        self.numCompletedRoomsBeforeDest = 0

        self.numMapCellsPerSide = len(self.map)
        self.mapCellSize = MAP_SIZE//self.numMapCellsPerSide

        self.MAP_TLx = self.centerX - (self.numMapCellsPerSide//2 * self.mapCellSize)
        self.MAP_TLy = self.centerY - (self.numMapCellsPerSide//2 * self.mapCellSize)

        self.initializeRoomRects()
        self.initializeRoomIcons()
    #------------------------------#

    #------------------------------#
    # Destructor Function
    def __del__(self):
        for rect in self.roomRects:
            rect.__del__()

        for icon in self.roomIcons:
            icon.__del__()

        super().__del__()
    #------------------------------#

    #------------------------------#
    # Function that initializes the Interactive Rects for the rooms
    def initializeRoomRects(self):
        # Iterate through each row of the map, initializing an interactive rect for each "r" cell
        for rowIndex, row in enumerate(self.map):
            for colIndex, col in enumerate(row):
                if col == "r":
                    cellRectTLx = self.MAP_TLx + (self.mapCellSize * colIndex)
                    cellRectTLy = self.MAP_TLy + (self.mapCellSize * rowIndex)
                    roomColor = ROOM_COLOR

                    # If the room happens to be your current location, color it accordingly
                    if rowIndex == self.currentLocation[0] and colIndex == self.currentLocation[1]:
                        roomColor = CURRENT_ROOM_COLOR

                    # Initialize the interactive rect, set a signal listener, and add it to the array of room rects
                    roomRect = InteractiveRect(cellRectTLx, cellRectTLy, self.mapCellSize, self.mapCellSize, defaultColor=roomColor, highlightColor=roomColor, text=None, parentID=self.gameObjectID, callbackArg=(rowIndex, colIndex))

                    self.setSignalListener(msg="clicked", sourceID=roomRect.getGameObjectID(), callback=self.roomSelected)

                    self.roomRects.append(roomRect)

                    # Icon stuff - basically calculate the coordinates for each room icon on the screen
                    for room in self.roomData:
                        # We only show icons for rooms that have NOT been completed
                        if not (room["completed"]):
                            if rowIndex == room["coordinates"][0] and colIndex == room["coordinates"][1]:
                                for icon in self.mapIconInfo:
                                    if (icon["name"] == room["type"]):
                                        self.roomIconInfo.append({"iconInfo": icon, "coordinates": (cellRectTLx + self.mapCellSize//2, cellRectTLy + self.mapCellSize//2)})
                                        break

                                break
    #------------------------------#

    #------------------------------#
    # Function that initializes the map room icons                       
    def initializeRoomIcons(self):
        for info in self.roomIconInfo:
            if info["iconInfo"]["name"] == "Boss":
                icon = Icon(info["iconInfo"]["assetPath"], info["coordinates"][0], info["coordinates"][1], scale=1.5, zIndex=self.zIndex+1)
            else:
                icon = Icon(info["iconInfo"]["assetPath"], info["coordinates"][0], info["coordinates"][1], width=32, height=32, zIndex=self.zIndex+1)
            self.roomIcons.append(icon)
    #------------------------------#

    #------------------------------#
    # Function that renders the map on the screen
    def render(self, canvas):
        # Draw the map cells
        for rowIndex, row in enumerate(self.map):
            for colIndex, col in enumerate(row):
                cellRectTLx = self.MAP_TLx + (self.mapCellSize * colIndex)
                cellRectTLy = self.MAP_TLy + (self.mapCellSize * rowIndex)
                mapCellRect = pygame.Rect(cellRectTLx, cellRectTLy, self.mapCellSize, self.mapCellSize)
                cellColor = MAP_BACKGROUND

                # If the cell is a hallway
                if col == "h":
                    cellColor = HALLWAY_COLOR
                    pygame.draw.rect(canvas, cellColor, mapCellRect)

                # if the cell is nothing
                if col == "_":
                    pygame.draw.rect(canvas, cellColor, mapCellRect)
    #------------------------------#

    #------------------------------#
    # Function that is called when a room is selected
    def roomSelected(self, roomCoordinates):
        # See if a path exists between the two rooms
        canMoveToRoom = self.pathExistsBetweenNodes(start=(self.currentLocation[0],self.currentLocation[1]), dest=roomCoordinates)

        # Double check that it's actually a true success case (basically just accounting for a very specific edge case here)
        if ((not self.getRoomCompletionStatus((self.currentLocation[0],self.currentLocation[1]))) and (not self.getRoomCompletionStatus(roomCoordinates)) and self.numCompletedRoomsBeforeDest == 0):
            canMoveToRoom = False

        # Reset the global values used in the pathfinding algorithm
        self.processedNodes = []
        self.numCompletedRoomsBeforeDest = 0

        # If the user can move to the room, emit a signal saying so
        if canMoveToRoom:
            self.emitSignal(msg="move-to-room", data=roomCoordinates, targetID=self.parentID)
    #------------------------------#
            
    #------------------------------#
    # Function that determines if a path exists between two specified rooms on the map   
    def pathExistsBetweenNodes(self, start, dest):
        # If the start and desitination are the same, simply return True
        if (start == dest):
            return True

        # Add the current node we're examining to the global processed nodes array so we don't process it again
        # in another layer of recursion
        self.processedNodes.append(start)

        # Get viable neighbors for the current node
        viableNeighbors = self.getViableNeighbors(start, dest)

        # If the destination is a viable neighbor, return True
        if (dest in viableNeighbors):
            return True

        # Remove any neighbors that have already been processed
        for neighbor in viableNeighbors:
            if (neighbor in self.processedNodes):
                viableNeighbors.remove(neighbor)
                

        # For each viable neighbor, call this function again
        # (Note: This is definitely a brute force search algorithm, but it at least looks clean because of recursion :) )
        for neighbor in viableNeighbors:
            if (self.pathExistsBetweenNodes(neighbor, dest)):
                # If the neighbor was a room and a path existed, add one to the number of completed rooms between the start and the destination
                if (self.map[neighbor[0]][neighbor[1]] == "r"):
                    self.numCompletedRoomsBeforeDest += 1
                return True

        # If nothing panned out, simply return false
        return False
    #------------------------------#

    #------------------------------#
    # Function that returns the viable neighbor nodes of a specified nodes
    def getViableNeighbors(self, node, dest):
        nodeRow = node[0]
        nodeCol = node[1]

        viableNeighbors = []

        # Checking horizontally
        if (nodeCol > 0):
            if (self.map[nodeRow][nodeCol-1] != "_"):
                if self.getRoomCompletionStatus((nodeRow, nodeCol-1)) or (nodeRow, nodeCol-1) == dest:
                    viableNeighbors.append((nodeRow, nodeCol-1))

        if (nodeCol < len(self.map[nodeRow]) - 1):
            if (self.map[nodeRow][nodeCol+1] != "_"):
                if self.getRoomCompletionStatus((nodeRow, nodeCol+1)) or (nodeRow, nodeCol+1) == dest:
                    viableNeighbors.append((nodeRow, nodeCol+1))

        # Checking vertically
        if (nodeRow > 0):
            if (self.map[nodeRow-1][nodeCol] != "_"):
                if self.getRoomCompletionStatus((nodeRow-1, nodeCol)) or (nodeRow-1, nodeCol) == dest:
                    viableNeighbors.append((nodeRow-1, nodeCol))

        if (nodeRow < len(self.map) - 1):
            if (self.map[nodeRow+1][nodeCol] != "_"):
                if self.getRoomCompletionStatus((nodeRow+1, nodeCol)) or (nodeRow+1, nodeCol) == dest:
                    viableNeighbors.append((nodeRow+1, nodeCol))

        return viableNeighbors
    #------------------------------#

    #------------------------------#
    # Function that gets the room completion status of a specified room/node on the map
    def getRoomCompletionStatus(self, room):
        if self.map[room[0]][room[1]] == "_":
            return False

        if self.map[room[0]][room[1]] == "h":
            return True
        
        for r in self.roomData:
            if r["coordinates"][0] == room[0] and r["coordinates"][1] == room[1]:
                return r["completed"]
        
        return False
    #------------------------------#
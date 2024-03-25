import pygame
from .game_object import GameObject
from .interactive_rect import InteractiveRect
from constants import *

# Class that implements the Items Window in the Battle Interface
class ItemsWindow(GameObject):
    #------------------------------#
    # Constructor Function
    def __init__(self, TLx=0, TLy=0, width=0, height=0, zIndex=10, parentID=""):
        super().__init__(zIndex=zIndex)
        self.parentID = parentID
        self.TLx = TLx
        self.TLy = TLy
        self.width = width
        self.height = height
        self.itemGroups = []
        self.itemOptions = []
        self.backButton = None
        self.font = pygame.font.Font(GAME_FONT_PATH, MED_FONT_SIZE)
        self.groupItems()
        self.initializeElements()
    #------------------------------#

    #------------------------------#
    # Destructor Function
    def __del__(self):
        self.backButton.__del__()
        
        for option in self.itemOptions:
            option.__del__()

        super().__del__()
    #------------------------------#

    #------------------------------#
    # Function that initializes all the UI elements
    def initializeElements(self):
        # Initialize the Back Button and set a signal listener
        backButtonTLx = self.TLx + 5
        backButtonTLy = self.TLy + 5
        backButtonTextWidth, backButtonTextHeight = self.font.size("<- Back")

        self.backButton = InteractiveRect(TLx=backButtonTLx, TLy=backButtonTLy, defaultColor=BATTLE_OPTIONS_BACKGROUND_COLOR, highlightColor=BATTLE_OPTIONS_BACKGROUND_COLOR, defaultTextColor=WHITE, highlightTextColor=BATTLE_TEXT_HIGHLIGHT_COLOR, text="<- Back", textCoordinates=(backButtonTLx, backButtonTLy), width=backButtonTextWidth, height=backButtonTextHeight, fontSize=MED_FONT_SIZE, parentID=self.gameObjectID, callbackArg="back", zIndex=11)

        self.setSignalListener(msg="clicked", sourceID=self.backButton.getGameObjectID(), callback=self.close)

        # Initialize the columns of items
        rightmostOption = backButtonTLx + backButtonTextWidth + 20

        for colIndex, col in enumerate(self.itemCols):

            lastOptionTLy = backButtonTLy + backButtonTextHeight
            largestWidth = 0

            for itemIndex, item in enumerate(col):
                # Initialize the option
                optionButtonTLx = rightmostOption
                optionButtonTLy = lastOptionTLy + 10
                optionText = item["name"] + "......x" + str(item["count"])
                optionTextWidth, optionTextHeight = self.font.size(optionText)

                option = InteractiveRect(TLx=optionButtonTLx, TLy=optionButtonTLy, defaultColor=BATTLE_OPTIONS_BACKGROUND_COLOR, highlightColor=BATTLE_OPTIONS_BACKGROUND_COLOR, defaultTextColor=WHITE, highlightTextColor=BATTLE_TEXT_HIGHLIGHT_COLOR, text=optionText, textCoordinates=(optionButtonTLx, optionButtonTLy), width=optionTextWidth, height=optionTextHeight, fontSize=MED_FONT_SIZE, parentID=self.gameObjectID, callbackArg=item["name"], zIndex=11)

                # Set a signal listener for when a user clicks an item
                self.setSignalListener(msg="clicked", sourceID=option.getGameObjectID(), callback=self.itemSelected)

                # Add the option to the list of item options
                self.itemOptions.append(option)

                # Calculate the TLy of the last option
                lastOptionTLy = optionButtonTLy + optionTextHeight

                # Set the largest width if appropriate
                if optionTextWidth > largestWidth:
                    largestWidth = optionTextWidth

            rightmostOption += largestWidth + 80
    #------------------------------#

    #------------------------------#
    # Function that creates an array of groups by item type in the user's inventory
    def groupItems(self):
        character = self.getGlobalDictValue("character")
        inventory = character["inventory"]
        
        # Compile the list of item groups based on what is in the character's inventory
        itemGroups = []
        for item in inventory:
            # Don't show 'Boss Key' or 'Auto-Revive' items
            if item["name"] == "Boss Key" or item["name"] == "Auto-Revive":
                continue

            # Find the corresponding item group if it exists
            groupFound = False
            for group in itemGroups:
                if group["name"] == item["name"]:
                    group["count"] += 1
                    groupFound = True

                if groupFound:
                    break

            # Create a group if one was not found
            if not groupFound:
                itemGroups.append({"name": item["name"], "count": 1})

        # Split the item groups into sets of three (there will be a max of three item groups in each column in the window)
        self.itemCols = []
        for i in range(0, len(itemGroups), 3):
            self.itemCols.append(itemGroups[i: i + 3])
    #------------------------------#

    #------------------------------#
    # Function that renders the window
    def render(self, canvas):
        # Draw the items rectangle and its border rectangle
        itemsWindowRect = pygame.Rect(self.TLx, self.TLy, self.width, self.height)
        pygame.draw.rect(canvas, BATTLE_OPTIONS_BACKGROUND_COLOR, itemsWindowRect)
        pygame.draw.rect(canvas, WHITE, itemsWindowRect, 2)
    #------------------------------#

    #------------------------------#
    # Function that is called whenever the user presses the "<- Back" button
    def close(self, _):
        # Emit the "close-window" signal to the parent game object
        self.emitSignal(msg="close-window", data=None, targetID=self.parentID)
    #------------------------------#

    #------------------------------#
    # Function that is called whenever a user selects an item
    def itemSelected(self, itemName):
        # Emit the "use-item" signal to the parent game object
        self.emitSignal(msg="use-item", data=itemName, targetID=self.parentID)
    #------------------------------#
        

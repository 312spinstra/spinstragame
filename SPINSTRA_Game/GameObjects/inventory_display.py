import pygame
from .game_object import GameObject
from .interactive_rect import InteractiveRect
from .simple_text import SimpleText
from .icon import Icon
from .item_info_window import ItemInfoWindow
from constants import *

# Class that implements the Inventory Display on the Map Overview screen
class InventoryDisplay(GameObject):
    #------------------------------#
    # Constructor Function
    def __init__(self, parentID="", zIndex=0):
        super().__init__(zIndex=zIndex)
        self.parentID = parentID
        self.itemFont = pygame.font.Font(GAME_FONT_PATH, SM_FONT_SIZE)
        self.labelFont = pygame.font.Font(GAME_FONT_PATH, MED_FONT_SIZE)
        self.inventoryLabel = None
        self.rectsDisabled = False
        self.infoWindow = None
        self.inventoryRows = []
        self.itemRects = []
        self.icons = []
        self.itemDisplaySpecs = []
        self.inventoryDisplayTLx = SCREEN_WIDTH - 400
        self.inventoryDisplayTLy = SCREEN_HEIGHT//2 - 200
        self.initializeElements()
    #------------------------------#

    #------------------------------#
    # Destructor Function
    def __del__(self):
        for rect in self.itemRects:
            rect.__del__()
        for icon in self.icons:
            icon.__del__()
        self.inventoryLabel.__del__()
        super().__del__()
    #------------------------------#

    #------------------------------#
    # Function that initializes all UI elements
    def initializeElements(self):
        self.groupItems()

        # Initialize the inventory label
        inventoryLabelText = "Inventory"
        inventoryLabelTextWidth, inventoryLabelTextHeight = self.labelFont.size(inventoryLabelText)

        inventoryLabelTLx = self.inventoryDisplayTLx + 100 - inventoryLabelTextWidth//2
        inventoryLabelTLy = self.inventoryDisplayTLy - 15 - inventoryLabelTextHeight

        self.inventoryLabel = SimpleText(text="Inventory", fontSize=MED_FONT_SIZE, x=inventoryLabelTLx, y=inventoryLabelTLy)

        # Initialize the item rectangles
        self.setupItemRectangles()

        # Initialize the item icons
        self.setupItemIcons()
    #------------------------------#

    #------------------------------#
    # Function that creates an array of groups by item type in the user's inventory
    def groupItems(self):
        character = self.getGlobalDictValue("character")
        inventory = character["inventory"]
        
        itemGroups = []

        for item in inventory:
            groupFound = False

            for group in itemGroups:
                if group["name"] == item["name"]:
                    group["count"] += 1
                    groupFound = True

                if groupFound:
                    break

            if not groupFound:
                itemGroups.append({"name": item["name"], "count": 1, "assetPath": item["assetPath"]})

        self.inventoryRows = []
        for i in range(0, len(itemGroups), 2):
            self.inventoryRows.append(itemGroups[i: i + 2])
    #------------------------------#

    #------------------------------#
    # Function that sets up the interactive rectangles the items are displayed in
    def setupItemRectangles(self, refresh=False):
        if refresh:
            for rect in self.itemRects:
                rect.__del__()
            for icon in self.icons:
                icon.__del__()
            self.itemRects = []
            self.itemDisplaySpecs = []
            self.groupItems()

        for rowIndex in range(4):
            for colIndex in range(2):
                itemRectTLx = self.inventoryDisplayTLx
                if colIndex == 1:
                    itemRectTLx += 100
                itemRectTLy = self.inventoryDisplayTLy + (100 * rowIndex)

                if (rowIndex < len(self.inventoryRows) and colIndex < len(self.inventoryRows[rowIndex])):
                    itemDisplaySpec = {"parentRectCoordinates": (itemRectTLx, itemRectTLy), "assetPath": self.inventoryRows[rowIndex][colIndex]["assetPath"]}

                    self.itemDisplaySpecs.append(itemDisplaySpec)

                    itemText = self.inventoryRows[rowIndex][colIndex]["name"] + "..x" + str(self.inventoryRows[rowIndex][colIndex]["count"])
                    itemTextWidth, itemTextHeight = self.itemFont.size(itemText)
                    textCoordinates = (itemRectTLx + 50 - itemTextWidth//2, itemRectTLy + 100 - itemTextHeight - 5)

                    itemRect = InteractiveRect(itemRectTLx, itemRectTLy, width=100, height=100, outlineOnly=True, highlightColor=BLUE, defaultTextColor=WHITE, highlightTextColor=WHITE, text=itemText, textCoordinates=textCoordinates, callbackArg=self.inventoryRows[rowIndex][colIndex]["name"], parentID=self.gameObjectID, fontSize=SM_FONT_SIZE)

                    self.itemRects.append(itemRect)

                    itemRectID = itemRect.getGameObjectID()
                    self.setSignalListener(msg="clicked", sourceID=itemRectID, callback=self.itemSelected)
                else:
                    itemRect = InteractiveRect(itemRectTLx, itemRectTLy, width=100, height=100, outlineOnly=True, text=None, highlightColor=WHITE)
                    self.itemRects.append(itemRect)

        if refresh:
            self.setupItemIcons()
    #------------------------------#
                    
    #------------------------------#
    # Function that initializes the Icon game objects in their proper place in the inventory
    def setupItemIcons(self):
        for spec in self.itemDisplaySpecs:
            icon = Icon(sourceFile=spec["assetPath"], centerX=spec["parentRectCoordinates"][0] + 50, centerY=spec["parentRectCoordinates"][1] + 50, scale=2)

            self.icons.append(icon)
    #------------------------------#

    #------------------------------#
    # Function that is called when an item is selected
    def itemSelected(self, itemType):
        if not self.rectsDisabled:
            self.infoWindow = ItemInfoWindow(itemType=itemType, parentID=self.gameObjectID)

            infoWindowID = self.infoWindow.getGameObjectID()
            self.setSignalListener(msg="close", sourceID=infoWindowID, callback=self.closeItemInfoWindow)
            self.setSignalListener(msg="use-item", sourceID=infoWindowID, callback=self.useItem)

            self.disableRects()
    #------------------------------#

    #------------------------------#
    # Function that disables the click functionality of the item rectangles
    def disableRects(self):
        self.rectsDisabled = True
    #------------------------------#

    #------------------------------#
    # Function that enables the click functionality of the item rectangles
    def enableRects(self):
        self.rectsDisabled = False
    #------------------------------#

    #------------------------------#
    # Function that closes the item info window and re-enables click functionality
    def closeItemInfoWindow(self, _):
        infoWindowID = self.infoWindow.getGameObjectID()
        self.infoWindow.__del__()
        self.removeSignalListenerBySourceID(infoWindowID)

        self.enableRects()
    #------------------------------#

    #------------------------------#
    # Function that is called when a user chooses to use an item
    def useItem(self, itemType):
        character = self.getGlobalDictValue("character")

        actuallyUseItem = True

        # Apply the appropriate item effect
        if itemType == "Potion":
            if character["HP"] < 100:
                if character["HP"] + 30 > 100:
                    character["HP"] = 100
                else:
                    character["HP"] += 30
            else:
                actuallyUseItem = False
        if itemType == "Elixir":
            # Add one usage to the character's special ability
            if character["type"]["specialAbility"]["uses"] < 3:
                character["type"]["specialAbility"]["uses"] += 1
            else:
                actuallyUseItem = False

        # Remove one instance of the specified item from the user's inventory
        if actuallyUseItem:
            inventory = character["inventory"]

            for item in inventory:
                if item["name"] == itemType:
                    inventory.remove(item)
                    break

            # Refresh the inventory display
            self.setupItemRectangles(refresh=True)

        # Close the item info window
        self.closeItemInfoWindow(None)

        # Emit the "item-used" signal to the parent game object
        self.emitSignal(msg="item-used", data=None, targetID=self.parentID)
    #------------------------------#


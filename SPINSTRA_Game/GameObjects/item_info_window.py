import pygame
from .game_object import GameObject
from .interactive_rect import InteractiveRect
from .simple_text import SimpleText
from constants import *
from utils import *

# Class that implements the Item Info Window
class ItemInfoWindow(GameObject):
    #------------------------------#
    # Constructor Function
    def __init__(self, itemType="", centerX=SCREEN_WIDTH//2, centerY=SCREEN_HEIGHT//2, width=500, height=300, backgroundColor=BATTLE_OPTIONS_BACKGROUND_COLOR, borderColor=WHITE, parentID="", zIndex=10):
        super().__init__(zIndex=zIndex)
        self.parentID = parentID
        self.itemType = itemType
        self.itemEntry = {}
        self.centerX = centerX
        self.centerY = centerY
        self.width = width
        self.height = height
        self.TLx = self.centerX - self.width//2
        self.TLy = self.centerY - height//2
        self.backgroundColor = backgroundColor
        self.borderColor = borderColor
        self.closeButton = None
        self.itemDescriptionParts = []
        self.options = []
        self.optionButtons = []
        self.useButton = None
        self.title = None
        self.titleFont = pygame.font.Font(GAME_FONT_PATH, MED_FONT_SIZE)
        self.descriptionFont = pygame.font.Font(GAME_FONT_PATH, REG_FONT_SIZE)
        self.getItemInfo()
        self.initializeElements()
    #------------------------------#

    #------------------------------#
    # Destructor Function
    def __del__(self):
        for part in self.itemDescriptionParts:
            part.__del__()
        for button in self.optionButtons:
            button.__del__()
        self.title.__del__()
        self.closeButton.__del__()
        if self.useButton != None:
            self.useButton.__del__()
        super().__del__()
    #------------------------------#

    #------------------------------#
    # Function that gets the info associated with the specified item - to be displayed in the window
    def getItemInfo(self):
        if self.itemType == "Boss Key":
            self.itemEntry = {"name": "Boss Key", "assetPath": "Assets/Items/Boss_Key/Boss_Key.png", "description": "The key that opens the Boss Room at the end of the level. This item is automatically used upon entering the Boss Room.", "inBattleOnly": True}
        else:
            items = self.getGlobalDictValue("items")

            for item in items:
                if item["name"] == self.itemType:
                    self.itemEntry = item
                    break
    #------------------------------#

    #------------------------------#
    # Function that initializes all the UI elements
    def initializeElements(self):
        # Initialize the close button and set a signal listener
        closeButtonFont = pygame.font.Font(GAME_FONT_PATH, TITLE_FONT_SIZE)
        closeButtonTextWidth, closeButtonTextHeight = closeButtonFont.size("X")
        closeButtonTLx = self.TLx + self.width - closeButtonTextWidth - 5
        closeButtonTLy = self.TLy + 5

        self.closeButton = InteractiveRect(closeButtonTLx, closeButtonTLy, closeButtonTextWidth, closeButtonTextHeight, defaultColor=self.backgroundColor, highlightColor=self.backgroundColor, defaultTextColor=WHITE, highlightTextColor=BATTLE_TEXT_HIGHLIGHT_COLOR, fontSize=MED_FONT_SIZE, text="X", textCoordinates=(closeButtonTLx, closeButtonTLy), parentID=self.gameObjectID, callbackArg=True, zIndex=self.zIndex + 1)

        self.setSignalListener(msg="clicked", sourceID=self.closeButton.getGameObjectID(), callback=self.closeButtonClicked)

        # Initialize the title
        titleTLx = self.TLx + 5
        titleTLy = self.TLy + 5
        _, titleTextHeight = self.titleFont.size(self.itemType)

        self.title = SimpleText(self.itemType, x=titleTLx, y = titleTLy, fontSize=MED_FONT_SIZE, zIndex=self.zIndex+1)

        # Initialize the description parts
        self.descriptionTextParts = prepareTextForRendering(self.itemEntry["description"], REG_FONT_SIZE, self.width-10)

        _, textHeight = self.descriptionFont.size(self.itemEntry["description"])
        textTLx = self.TLx + 5
        textStartingTLy = self.TLy + titleTextHeight + 15

        for index, part in enumerate(self.descriptionTextParts):
            descriptionPart = SimpleText(part, x=textTLx, y = textStartingTLy + ((5 + textHeight) * index), fontSize=REG_FONT_SIZE, zIndex=self.zIndex+1)
            self.itemDescriptionParts.append(descriptionPart)

        # Initialize the option buttons
        optionRowCenterX = self.centerX
        optionRowCenterY= self.centerY + self.height//2 - 15
        optionPaddingBetween = 10
        optionZIndex = self.zIndex + 1

        # Initialize the "Use" button and set a signal listener
        buttonFont = pygame.font.Font(GAME_FONT_PATH, MED_FONT_SIZE)
        buttonTextWidth, buttonTextHeight = buttonFont.size("Use")

        if not self.itemEntry["inBattleOnly"]:
            useButtonWidth = buttonTextWidth + 10
            useButtonHeight = buttonTextHeight + 8
            useButtonTLx = self.centerX - buttonTextWidth//2
            useButtonTLy = self.centerY + self.height//2 - 15 - useButtonHeight
            useButtonTextCoordinates = (useButtonTLx + 5, useButtonTLy + 4)

            self.useButton = InteractiveRect(useButtonTLx, useButtonTLy, useButtonWidth, useButtonHeight, defaultColor=self.backgroundColor, highlightColor=WHITE, defaultTextColor=WHITE, highlightTextColor=self.backgroundColor, parentID=self.gameObjectID, text="Use", textCoordinates=useButtonTextCoordinates, fontSize=MED_FONT_SIZE, callbackArg="Use", zIndex=self.zIndex+1)

            self.setSignalListener(msg="clicked", sourceID=self.useButton.getGameObjectID(), callback=self.useButtonClicked)
    #------------------------------#

    #------------------------------#
    # Function that renders the item info windows
    def render(self, canvas):
        # Render the background and border rectangles
        backgroundRect = pygame.Rect(self.TLx, self.TLy, self.width, self.height)
        borderRect = pygame.Rect(self.TLx, self.TLy, self.width, self.height)

        pygame.draw.rect(canvas, self.backgroundColor, backgroundRect)
        pygame.draw.rect(canvas, self.borderColor, borderRect, 2)
    #------------------------------#

    #------------------------------#
    # Function that is called when the close button is clicked
    def closeButtonClicked(self, _):
        self.emitSignal(msg="close", data=None, targetID=self.parentID)
    #------------------------------#

    #------------------------------#
    # Function that is called when the use button is clicked
    def useButtonClicked(self, _):
        self.emitSignal(msg="use-item", data=self.itemType, targetID=self.parentID)
    #------------------------------#

import pygame
from .game_object import GameObject
from .interactive_rect import InteractiveRect
from .simple_text import SimpleText
from constants import *
from utils import *

# Class that implements a menu
class Menu(GameObject):
    #------------------------------#
    # Constructor Function
    def __init__(self, title, options, parentID=None, isPauseMenu=False):
        super().__init__()
        self.titleText = title
        self.title = None
        self.options = options
        self.optionElements = []
        self.selectedOptionIndex = -1
        self.parentID = parentID
        self.isPauseMenu = isPauseMenu
        self.titleFont = pygame.font.Font(GAME_FONT_PATH, TITLE_FONT_SIZE)
        self.font = pygame.font.Font(GAME_FONT_PATH, REG_FONT_SIZE)
        self.initializeOptions()
    #------------------------------#

    #------------------------------#
    # Destructor Function - delete all interactive menu options along with the menu object
    def __del__(self):
        self.title.__del__()

        for el in self.optionElements:
            el["rect"].__del__()

        super().__del__()
    #------------------------------#

    #------------------------------#
    # Function that initializes the interactive menu options
    def initializeOptions(self):
        # Initialize the menu title
        titleTextWidth, _ = self.titleFont.size(self.titleText)
        titleTLx = SCREEN_WIDTH//2 - titleTextWidth//2
        titleTLy = 215
        self.title = SimpleText(text=self.titleText, fontSize=TITLE_FONT_SIZE, x=titleTLx, y=titleTLy)

        # Initialize the menu options and set signal listeners for each
        for index, option in enumerate(self.options):
            optionTextWidth, optionTextHeight = self.font.size(option)
            textTLx = SCREEN_WIDTH//2 - optionTextWidth//2
            textTLy = SCREEN_HEIGHT//2 + (index * (optionTextHeight + 8))

            optionRect = InteractiveRect(textTLx, textTLy, optionTextWidth, optionTextHeight, defaultColor=BLACK, highlightColor=WHITE, defaultTextColor=WHITE, highlightTextColor=BLACK, parentID=self.gameObjectID, text=option, textCoordinates=(textTLx, textTLy), callbackArg=option)
            
            element = {"value": option, "rect": optionRect}
            self.optionElements.append(element)

            self.setSignalListener(msg="clicked", sourceID=optionRect.getGameObjectID(), callback=self.optionClicked)
    #------------------------------#

    #------------------------------#
    # Function that is called when an option is clicked
    def optionClicked(self, option):
        self.emitSignal("option-selected", option, self.parentID)
    #------------------------------#

    #------------------------------#
    # Function that returns the Game Object IDs for each of the menu options
    def getOptionGameObjectIDs(self):
        if self.isPauseMenu:
            optionIDs = []
            for el in self.optionElements:
                optionID = el["rect"].getGameObjectID()
                optionIDs.append(optionID)

            optionIDs.append(self.title.getGameObjectID())

            return optionIDs
        else:
            return []
    #------------------------------#
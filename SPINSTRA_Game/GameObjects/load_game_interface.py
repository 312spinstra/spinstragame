import pygame
from .game_object import GameObject
from .textbox import Textbox
from .simple_text import SimpleText
from .battle_info_window import BattleInfoWindow
from .interactive_rect import InteractiveRect
from constants import *

# Class that implements the interface that allows users to load previous saved games
class LoadGameInterface(GameObject):
    #------------------------------#
    # Constructor Function
    def __init__(self, parentID=""):
        super().__init__()
        self.parentID = parentID
        self.elements = []
        self.infoWindow = None
        self.backButton = None
        self.backButtonText = "<- Back"
        self.regularFont = pygame.font.Font(GAME_FONT_PATH, REG_FONT_SIZE)
        self.labelFont = pygame.font.Font(GAME_FONT_PATH, MED_FONT_SIZE)
        self.largeFont = pygame.font.Font(GAME_FONT_PATH, TITLE_FONT_SIZE)
        self.initializeElements()
    #------------------------------#

    #------------------------------#
    # Destructor function
    def __del__(self):
        for el in self.elements:
            el.__del__()

        if (self.infoWindow != None):
            self.infoWindow.__del__()

        if (self.backButton != None):
            self.backButton.__del__()

        super().__del__()
    #------------------------------#

    #------------------------------#
    # Function that initializes the elements used by the character file password input screen
    def initializeElements(self):
        # Intialize the character password textbox and set a signal listener
        _, regularCharHeight = self.regularFont.size("A")
        textboxHeight = regularCharHeight + 8
        characterPasswordTextbox_TLx = SCREEN_WIDTH//2
        characterPasswordTextbox_TLy = SCREEN_HEIGHT//2 - textboxHeight//2
        characterPasswordTextbox = Textbox(characterPasswordTextbox_TLx, characterPasswordTextbox_TLy, parentID=self.gameObjectID)
        self.elements.append(characterPasswordTextbox)

        self.setSignalListener(msg="submitted", sourceID=characterPasswordTextbox.getGameObjectID(), callback=self.characterPasswordSubmitted)

        # Initialize the character password textbox label
        characterPasswordLabelWidth, characterPasswordLabelHeight = self.labelFont.size("PASSWORD:")
        characterPasswordLabelTLx = characterPasswordTextbox_TLx - characterPasswordLabelWidth - 10
        characterPasswordLabelTLy = SCREEN_HEIGHT//2 - characterPasswordLabelHeight//2

        characterPasswordLabel = SimpleText("PASSWORD:", fontSize=MED_FONT_SIZE, x=characterPasswordLabelTLx, y=characterPasswordLabelTLy)
        self.elements.append(characterPasswordLabel)

        # Initialize the back button and set a signal listener
        backButtonTextWidth, backButtonTextHeight = self.largeFont.size(self.backButtonText)
        backButtonTLx = 5
        backButtonTLy = 15
        self.backButton = InteractiveRect(backButtonTLx, backButtonTLy, width=backButtonTextWidth, height=backButtonTextHeight, defaultColor=BLACK, highlightColor=BLACK, defaultTextColor=WHITE, highlightTextColor=BATTLE_TEXT_HIGHLIGHT_COLOR, parentID=self.gameObjectID, text=self.backButtonText, textCoordinates=(backButtonTLx, backButtonTLy), fontSize=TITLE_FONT_SIZE, callbackArg="back")

        self.setSignalListener(msg="clicked", sourceID=self.backButton.getGameObjectID(), callback=self.backButtonClicked)
    #------------------------------#

    #------------------------------#
    # Function that is called when the password is submitted
    def characterPasswordSubmitted(self, password):
        loadStatus = self.loadGame(password)
        
        # If the game loaded successfully, emit a signal to the parent, otherwise show an error message to the user
        if loadStatus:
            self.emitSignal(msg="game-loaded", data=None, targetID=self.parentID)
        else:
            self.infoWindow = BattleInfoWindow("Password is incorrect!", centerY=200, parentID=self.gameObjectID)
            self.setSignalListener(msg="close", sourceID=self.infoWindow.getGameObjectID(), callback=self.closeInfoWindow)
    #------------------------------#

    #------------------------------#
    # Function that is called to close the info window       
    def closeInfoWindow(self, _):
        self.removeSignalListenerBySourceID(self.infoWindow.getGameObjectID())
        self.infoWindow.__del__()
    #------------------------------#

    #------------------------------#
    # Function that is called when the back button is clicked   
    def backButtonClicked(self, _):
        self.emitSignal(msg="close-load-interface", data=None, targetID=self.parentID)
    #------------------------------#
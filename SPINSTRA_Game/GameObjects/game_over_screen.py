import pygame
from .game_object import GameObject
from .interactive_rect import InteractiveRect
from .simple_text import SimpleText
from constants import *

# Class that implements the "Game Over" screen
class GameOverScreen(GameObject):
    #------------------------------#
    # Constructor Function
    def __init__(self, parentID=""):
        super().__init__()
        self.parentID = parentID
        self.elements = []
        self.initializeElements()
    #------------------------------#

    #------------------------------#
    # Destructor function
    def __del__(self):
        for el in self.elements:
            el.__del__()
        super().__del__()
    #------------------------------#

    #------------------------------#
    # Function that initializes the UI elements
    def initializeElements(self):
        # Initialize the title
        titleFont = pygame.font.Font(GAME_FONT_PATH, TITLE_FONT_SIZE)
        gameOverTextWidth, gameOverTextHeight = titleFont.size("Game Over")

        gameOverTextTLx = SCREEN_WIDTH//2 - gameOverTextWidth//2
        gameOverTextTLy = SCREEN_HEIGHT//2 - gameOverTextHeight//2

        gameOverText = SimpleText("Game Over", fontSize=TITLE_FONT_SIZE, x=gameOverTextTLx, y=gameOverTextTLy)
        self.elements.append(gameOverText)

        buttonFont = pygame.font.Font(GAME_FONT_PATH, REG_FONT_SIZE)

        # Initialize the "Return to Main Menu" button and set a signal listener
        returnToMainMenuTextWidth, returnToMainMenuTextHeight = buttonFont.size("Return to Main Menu")
        returnToMainMenuButtonTLx = SCREEN_WIDTH//2 - returnToMainMenuTextWidth//2
        returnToMainMenuButtonTLy = gameOverTextTLy + gameOverTextHeight + 15

        returnToMainMenuButton = InteractiveRect(returnToMainMenuButtonTLx, returnToMainMenuButtonTLy, returnToMainMenuTextWidth, returnToMainMenuTextHeight, defaultColor=BLACK, highlightColor=WHITE,  defaultTextColor=WHITE, highlightTextColor=BLACK, text="Return To Main Menu", textCoordinates=(returnToMainMenuButtonTLx, returnToMainMenuButtonTLy), fontSize=REG_FONT_SIZE, parentID=self.gameObjectID)

        self.setSignalListener(msg="clicked", sourceID=returnToMainMenuButton.getGameObjectID(), callback=self.returnToMainMenu)
        self.elements.append(returnToMainMenuButton)

        # Initialize the "Quit" button and set a signal listener
        quitTextWidth, quitTextHeight = buttonFont.size("Quit")
        quitButtonTLx = SCREEN_WIDTH//2 - quitTextWidth//2
        quitButtonTLy = returnToMainMenuButtonTLy + returnToMainMenuTextHeight + 10

        quitButton = InteractiveRect(quitButtonTLx, quitButtonTLy, quitTextWidth, quitTextHeight, defaultColor=BLACK, highlightColor=WHITE, defaultTextColor=WHITE, highlightTextColor=BLACK, text="Quit", textCoordinates=(quitButtonTLx, quitButtonTLy), fontSize=REG_FONT_SIZE, parentID=self.gameObjectID)

        self.setSignalListener(msg="clicked", sourceID=quitButton.getGameObjectID(), callback=self.quitGame)
        self.elements.append(quitButton)
    #------------------------------#
        
    #------------------------------#
    # Function that emits the "Return to Main Menu" signal
    def returnToMainMenu(self, _):
        self.emitSignal(msg="return-to-main-menu", data=None, targetID=self.parentID)
    #------------------------------#

    #------------------------------#
    # Function that emits the "Quit Game" signal
    def quitGame(self, _):
        self.emitSignal(msg="quit-game", data=None, targetID=self.parentID)
    #------------------------------#
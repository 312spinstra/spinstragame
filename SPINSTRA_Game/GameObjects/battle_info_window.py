import pygame
import time
from .game_object import GameObject
from .interactive_rect import InteractiveRect
from .simple_text import SimpleText
from constants import *
from utils import *

# Class that implements the Battle Info Window
class BattleInfoWindow(GameObject):
    #------------------------------#
    # Constructor Function
    def __init__(self, info="", secondsUntilClose=1, callbackArg=None, centerX=SCREEN_WIDTH//2, centerY=SCREEN_HEIGHT//2-100, width=500, height=300, backgroundColor=BATTLE_OPTIONS_BACKGROUND_COLOR, borderColor=WHITE, parentID="", zIndex=10):
        super().__init__(zIndex=zIndex)
        self.parentID = parentID
        self.infoText = info
        self.secondsUntilClose = secondsUntilClose
        self.callbackArg = callbackArg
        self.timeToClose = None
        self.centerX = centerX
        self.centerY = centerY
        self.width = width
        self.height = height
        self.TLx = self.centerX - self.width//2
        self.TLy = self.centerY - height//2
        self.backgroundColor = backgroundColor
        self.borderColor = borderColor
        self.info = None
        self.infoFont = pygame.font.Font(GAME_FONT_PATH, MED_FONT_SIZE)
        self.initializeElements()
    #------------------------------#

    #------------------------------#
    # Destructor Function
    def __del__(self):
        self.info.__del__()
        super().__del__()
    #------------------------------#

    #------------------------------#
    # Function that initializes all the UI elements
    def initializeElements(self):
        # Initialize the Info
        infoTextWidth, infoTextHeight = self.infoFont.size(self.infoText)
        infoTLx = self.centerX - infoTextWidth//2
        infoTLy = self.centerY - infoTextHeight//2

        self.info = SimpleText(self.infoText, x=infoTLx, y=infoTLy, fontSize=MED_FONT_SIZE, zIndex=self.zIndex+1)

        # Figure out what time the window should close
        self.timeToClose = time.time() + self.secondsUntilClose
    #------------------------------#

    #------------------------------#
    # Function that renders the item info windows
    def render(self, canvas):
        # Render the background and border rectangles
        backgroundRect = pygame.Rect(self.TLx, self.TLy, self.width, self.height)
        borderRect = pygame.Rect(self.TLx, self.TLy, self.width, self.height)

        pygame.draw.rect(canvas, self.backgroundColor, backgroundRect)
        pygame.draw.rect(canvas, self.borderColor, borderRect, 2)

        # If it's time to close, go ahead and close
        now = time.time()
        if (now >= self.timeToClose):
            self.close()
    #------------------------------#

    #------------------------------#
    # Function that emits a close signal to the parent
    def close(self):
        self.emitSignal(msg="close", data=self.callbackArg, targetID=self.parentID)
    #------------------------------#

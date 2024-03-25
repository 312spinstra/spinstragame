import pygame
from .game_object import GameObject
from constants import *

# Class that implements a simple text display
class SimpleText(GameObject):
    #------------------------------#
    # Constructor Function
    def __init__(self, text="", fontSize=REG_FONT_SIZE, x=0, y=0, textColor=WHITE, behavior=None, zIndex=0):
        super().__init__(zIndex=zIndex)
        self.text = text
        self.x = x
        self.y = y
        self.textColor = textColor
        self.behavior = behavior
        self.font = pygame.font.Font(GAME_FONT_PATH, fontSize)
        self.textSurface = None
        self.initializeElement()
    #------------------------------#

    #------------------------------#
    # Function that initializes the text surface to be rendered
    def initializeElement(self):
        self.textSurface = self.font.render(self.text, True, self.textColor)
        if self.behavior != None:
            if self.behavior == "horizontal-shift-left":
                self.x -= self.textSurface.get_width()
            if self.behavior == "horizontal-shift-right":
                self.x += self.textSurface.get_width()
            if self.behavior == "center":
                self.x -= self.textSurface.get_width()//2
                self.y -= self.textSurface.get_height()//2
    #------------------------------#

    #------------------------------#
    # Function that renders the text on the screen
    def render(self, canvas):
        if (hasattr(self, "textSurface")):
            if self.textSurface != None:
                canvas.blit(self.textSurface, (self.x, self.y))
    #------------------------------#
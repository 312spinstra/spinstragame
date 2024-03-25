import pygame
from .game_object import GameObject
from constants import *

# Class that implements an interactive rectangle
class InteractiveRect(GameObject):
    #------------------------------#
    # Constructor Function
    def __init__(self, TLx=0, TLy=0, width=100, height=100, outlineOnly=False, defaultColor=WHITE, highlightColor=RED, defaultTextColor=BLACK, highlightTextColor=WHITE, parentID=None, text="", textCoordinates=None, fontSize=REG_FONT_SIZE, callbackArg=None, zIndex=0):
        super().__init__(zIndex=zIndex)
        self.TLx = TLx
        self.TLy = TLy
        self.width = width
        self.height = height
        self.hovered = False
        self.rect = None
        self.element = None
        self.outlineOnly = outlineOnly
        self.defaultColor = defaultColor
        self.highlightColor = highlightColor
        self.defaultTextColor = defaultTextColor
        self.highlightTextColor = highlightTextColor
        self.parentID = parentID
        self.font = pygame.font.Font(GAME_FONT_PATH, fontSize)
        self.text = text
        self.textCoordinates = textCoordinates
        self.callbackArg = callbackArg
        self.disabled = False
    #------------------------------#

    #------------------------------#
    # Function that renders the rectangle and any associated text
    def render(self, canvas):
        self.rect = pygame.Rect(self.TLx, self.TLy, self.width, self.height)
        color = self.defaultColor
        textColor = self.defaultTextColor
        if self.hovered:
            color = self.highlightColor
            textColor = self.highlightTextColor
        if self.outlineOnly:
            self.element = pygame.draw.rect(canvas, color, self.rect, 2)
        else:
            self.element = pygame.draw.rect(canvas, color, self.rect)

        if hasattr(self, "text") and self.text != None:
            textSurface = self.font.render(self.text, True, textColor)
            canvas.blit(textSurface, self.textCoordinates)
    #------------------------------#

    #------------------------------#
    # Function that handles user interaction
    def handleInteraction(self, event, action, mousePos):
        if action == "left-click":
            if self.element != None and (not self.disabled):
                if self.element.collidepoint(mousePos) and self.parentID != None:
                    self.emitSignal("clicked", self.callbackArg, self.parentID)

        if self.element != None:
            if self.element.collidepoint(mousePos):
                self.hovered = True
            else:
                self.hovered = False
    #------------------------------#

    #------------------------------#
    # Function that disables interactivity
    def disable(self):
        self.disabled = True
    #------------------------------#

    #------------------------------#
    # Function that enables interactivity
    def enable(self):
        self.disabled = False
    #------------------------------#

    #------------------------------#
    # Function that alters the text colors in the rectangle 
    def alterTextColors(self, newDefaultTextColor, newHighlightTextColor):
        self.defaultTextColor = newDefaultTextColor
        self.highlightTextColor = newHighlightTextColor
    #------------------------------#

    #------------------------------#
    # Function that alters the colors in the rectangle   
    def alterColors(self, newDefaultColor, newHighlightColor):
        self.defaultColor = newDefaultColor
        self.highlightColor = newHighlightColor
    #------------------------------#
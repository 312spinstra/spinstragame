import pygame
from .game_object import GameObject
from .simple_text import SimpleText
from constants import *

# Class that implements a basic Health Bar
class HealthBar(GameObject):
    #------------------------------#
    # Constructor Function
    def __init__(self, TLx=0, TLy=0, maxHealth=100, initialHealth=100, healthBarWidth=300, healthBarHeight=25, labelText="HP:", fontSize=MED_FONT_SIZE, parentID=""):
        super().__init__()
        self.parentID = parentID
        self.TLx = TLx
        self.TLy = TLy
        self.maxHealth = maxHealth
        self.currentHealth = initialHealth
        self.healthBarWidth = healthBarWidth
        self.healthBarHeight = healthBarHeight
        self.healthBarTLx = -1
        self.healthBarTLy = -1
        self.healthBarUnderside = None
        self.healthBar = None
        self.labelText = labelText
        self.fontSize = fontSize
        self.labelFont = pygame.font.Font(GAME_FONT_PATH, self.fontSize)
        self.label = None
        self.createLabel()
    #------------------------------#

    #------------------------------#
    # Destructor Function
    def __del__(self):
        if (self.label != None):
            self.label.__del__()
        super().__del__()
    #------------------------------#

    #------------------------------#
    # Function that initializes the health bar label
    def createLabel(self):
        labelWidth, labelHeight = self.labelFont.size(self.labelText)
        self.label = SimpleText(text=self.labelText, fontSize=self.fontSize, x=self.TLx, y=self.TLy - labelHeight//2)

        self.healthBarTLx = self.TLx + labelWidth + 5
        self.healthBarTLy = self.TLy - self.healthBarHeight//2
    #------------------------------#
        
    #------------------------------#
    # Function that renders the health bar on the screen
    def render(self, canvas):
        self.healthBarUnderside = pygame.Rect(self.healthBarTLx, self.healthBarTLy, self.healthBarWidth, self.healthBarHeight)
        self.healthBar = pygame.Rect(self.healthBarTLx, self.healthBarTLy, round((self.currentHealth/self.maxHealth) * self.healthBarWidth), self.healthBarHeight)
        pygame.draw.rect(canvas, RED, self.healthBarUnderside)
        pygame.draw.rect(canvas, GREEN, self.healthBar)
    #------------------------------#

    #------------------------------#
    # Function that updates the current health value
    def updateHealthValue(self, newHealthValue):
        self.currentHealth = newHealthValue
    #------------------------------#
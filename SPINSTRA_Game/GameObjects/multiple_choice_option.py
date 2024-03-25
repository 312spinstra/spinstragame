import pygame
from .game_object import GameObject
from .checkbox import Checkbox
from .simple_text import SimpleText
from constants import *

# Class that implements a multiple choice option
class MultipleChoiceOption(GameObject):
    #------------------------------#
    # Constructor Function
    def __init__(self, TLx=0, TLy=0, optionText="", zIndex=0, parentID=""):
        super().__init__(zIndex=zIndex)
        self.parentID = parentID
        self.coordinates = (TLx, TLy)
        self.optionText = optionText
        self.checkbox = None
        self.option = None
        self.initializeElements()
    #------------------------------#
    
    #------------------------------#
    # Destructor Function
    def __del__(self):
        self.checkbox.__del__()
        self.option.__del__()
        super().__del__()
    #------------------------------#

    #------------------------------#
    # Function that initializes the UI elements used in the Multiple Choice Option   
    def initializeElements(self):
        # Initialize the checkbox and set signal listeners
        self.checkbox = Checkbox(coordinates=self.coordinates, zIndex=self.getZIndex(), parentID=self.gameObjectID)
        checkboxID = self.checkbox.getGameObjectID()
        self.setSignalListener(msg="selected", sourceID=checkboxID, callback=self.optionSelected)
        self.setSignalListener(msg="deselected", sourceID=checkboxID, callback=self.optionDeselected)

        # Initialize the option text
        regFont = pygame.font.Font(GAME_FONT_PATH, REG_FONT_SIZE)
        _, optionTextHeight = regFont.size(self.optionText)
        optionTextTLx = self.coordinates[0] + 15 + 5
        optionTextTLy = self.coordinates[1] + 8 - optionTextHeight//2
        self.option = SimpleText(text=self.optionText, x=optionTextTLx, y=optionTextTLy, zIndex=self.getZIndex())
    #------------------------------#

    #------------------------------#
    # Function that is called when the option is selected 
    def optionSelected(self, _):
        self.emitSignal(msg="option-selected", data=self.optionText, targetID=self.parentID)
    #------------------------------#

    #------------------------------#
    # Function that is called when the option is deselected
    def optionDeselected(self, _):
        self.emitSignal(msg="option-deselected", data=self.optionText, targetID=self.parentID)
    #------------------------------#

    #------------------------------#
    # Function that deselects the option   
    def deselect(self):
        # Tell the checkbox to deselect itself
        self.checkbox.deselect()
    #------------------------------#
from .game_object import GameObject
from .interactive_rect import InteractiveRect
from constants import *

# Class that implements a checkbox input
class Checkbox(GameObject):
    #------------------------------#
    # Constructor Function
    def __init__(self, coordinates=(0,0), zIndex=0, parentID=""):
        super().__init__(zIndex=zIndex)
        self.parentID = parentID
        self.TLx = coordinates[0]
        self.TLy = coordinates[1]
        self.checkboxHeight = 16
        self.checkboxWidth = 16
        self.inputRect = None
        self.inputChecked = False
        self.initializeElements()
    #------------------------------#

    #------------------------------#
    # Destructor Function
    def __del__(self):
        self.inputRect.__del__()
        super().__del__()
    #------------------------------#

    #------------------------------#
    # Function that initialize the UI elements used in the checkbox
    def initializeElements(self):
        self.inputRect = InteractiveRect(self.TLx, self.TLy, width=self.checkboxHeight, height=self.checkboxWidth, text=None, defaultColor=WHITE, highlightColor=LIGHT_GREEN, zIndex=self.getZIndex(), parentID=self.gameObjectID)

        self.setSignalListener(msg="clicked", sourceID=self.inputRect.getGameObjectID(), callback=self.inputClicked)
    #------------------------------#

    #------------------------------#
    # Function that is called when the input is checked  
    def inputClicked(self, _):
        self.inputChecked = not self.inputChecked
        if self.inputChecked:
            newDefaultColor = GREEN
            newHighlightColor = LIGHT_GREEN
            self.emitSignal(msg="selected", data=None, targetID=self.parentID)
        else:
            newDefaultColor = WHITE
            newHighlightColor =  LIGHT_GREEN
            self.emitSignal(msg="deselected", data=None, targetID=self.parentID)

        self.inputRect.alterColors(newDefaultColor, newHighlightColor)
    #------------------------------#

    #------------------------------#
    # Function that manually deselects the checkbox  
    def deselect(self):
        self.inputChecked = False
        newDefaultColor = WHITE
        newHighlightColor =  LIGHT_GREEN
        self.inputRect.alterColors(newDefaultColor, newHighlightColor)
    #------------------------------#
import pygame
from .game_object import GameObject
from .interactive_rect import InteractiveRect
from constants import *

# WIDTH = 290
# HEIGHT = 180
# 4 items per column: 10px spacing between
# 15px padding on the sides

# Class that implements the Special Abilities Window in the Battle Interface
class SpecialAbilitiesWindow(GameObject):
    #------------------------------#
    # Constructor Function
    def __init__(self, TLx=0, TLy=0, width=0, height=0, zIndex=10, disallowedAbilities=[], parentID=""):
        super().__init__(zIndex=zIndex)
        self.parentID = parentID
        self.TLx = TLx
        self.TLy = TLy
        self.width = width
        self.height = height
        self.itemCols= []
        self.itemGroups = []
        self.abilityOptions = []
        self.specialAbilities = []
        self.disallowedAbilities = disallowedAbilities
        self.backButton = None
        self.font = pygame.font.Font(GAME_FONT_PATH, MED_FONT_SIZE)
        self.initializeSpecialAbilities()
        self.initializeElements()
    #------------------------------#

    #------------------------------#
    # Destructor Function
    def __del__(self):
        self.backButton.__del__()
        
        for option in self.abilityOptions:
            option["button"].__del__()

        super().__del__()
    #------------------------------#

    #------------------------------#
    # Function that initializes the list of special abilities
    def initializeSpecialAbilities(self):
        # Get the character class's special ability
        character = self.getGlobalDictValue("character")
        specialAbility = character["type"]["specialAbility"]

        # Initialize the special abilities list
        self.specialAbilities = []

        # Only add the class special ability to the list if the user has a use left
        if (specialAbility["uses"] >= 1):
            self.specialAbilities.append(specialAbility["name"])
        
        # Add the "Flee" ability if it's not explicity disallowed
        if (not("Flee" in self.disallowedAbilities)):
            self.specialAbilities.append("Flee")
    #------------------------------#

    #------------------------------#
    # Function that initializes all the UI elements
    def initializeElements(self):
        # Initialize the Back Button and set a signal listener
        backButtonTLx = self.TLx + 5
        backButtonTLy = self.TLy + 5
        backButtonTextWidth, backButtonTextHeight = self.font.size("<- Back")

        self.backButton = InteractiveRect(TLx=backButtonTLx, TLy=backButtonTLy, defaultColor=BATTLE_OPTIONS_BACKGROUND_COLOR, highlightColor=BATTLE_OPTIONS_BACKGROUND_COLOR, defaultTextColor=WHITE, highlightTextColor=BATTLE_TEXT_HIGHLIGHT_COLOR, text="<- Back", textCoordinates=(backButtonTLx, backButtonTLy), width=backButtonTextWidth, height=backButtonTextHeight, fontSize=MED_FONT_SIZE, parentID=self.gameObjectID, callbackArg="back", zIndex=11)

        self.setSignalListener(msg="clicked", sourceID=self.backButton.getGameObjectID(), callback=self.close)

        # Initialize the columns of items
        rightmostOption = backButtonTLx + backButtonTextWidth + 20

        lastOptionTLy = backButtonTLy + backButtonTextHeight

        for optionIndex, option in enumerate(self.specialAbilities):
            optionButtonTLx = backButtonTLx + backButtonTextWidth + 20
            optionButtonTLy = lastOptionTLy + 10
            optionText = option
            optionTextWidth, optionTextHeight = self.font.size(optionText)

            option = InteractiveRect(TLx=optionButtonTLx, TLy=optionButtonTLy, defaultColor=BATTLE_OPTIONS_BACKGROUND_COLOR, highlightColor=BATTLE_OPTIONS_BACKGROUND_COLOR, defaultTextColor=WHITE, highlightTextColor=BATTLE_TEXT_HIGHLIGHT_COLOR, text=optionText, textCoordinates=(optionButtonTLx, optionButtonTLy), width=optionTextWidth, height=optionTextHeight, fontSize=MED_FONT_SIZE, parentID=self.gameObjectID, callbackArg=option, zIndex=11)

            # Set the event listener for when a user clicks an item
            self.setSignalListener(msg="clicked", sourceID=option.getGameObjectID(), callback=self.abilitySelected)

            self.abilityOptions.append({"name": optionText, "button": option})

            lastOptionTLy = optionButtonTLy + optionTextHeight
    #------------------------------#

    #------------------------------#
    # Function that renders the window
    def render(self, canvas):
        # Draw the items rectangle and its border rectangle
        itemsWindowRect = pygame.Rect(self.TLx, self.TLy, self.width, self.height)
        pygame.draw.rect(canvas, BATTLE_OPTIONS_BACKGROUND_COLOR, itemsWindowRect)
        pygame.draw.rect(canvas, WHITE, itemsWindowRect, 2)
    #------------------------------#

    #------------------------------#
    # Function that is called whenever the user presses the "<- Back" button
    def close(self, _):
        self.emitSignal(msg="close-window", data=None, targetID=self.parentID)
    #------------------------------#

    #------------------------------#
    # Function that is called whenever a user selects an ability
    def abilitySelected(self, ability):
        self.emitSignal(msg="use-special-ability", data=ability, targetID=self.parentID)
    #------------------------------#

import math
import pygame
from .game_object import GameObject
from .interactive_rect import InteractiveRect
from .animated_sprite import AnimatedSprite
from .textbox import Textbox
from .simple_text import SimpleText
from constants import *
from utils import *

# Class that implements the Character Creator interface
class CharacterCreator(GameObject):
    #------------------------------#
    # Constructor Function
    def __init__(self, characterTypes, parentID=""):
        super().__init__()
        self.characterTypes = characterTypes
        self.parentID = parentID

        self.character = None

        self.characterTypeElements = []
        self.typeConfirmationElements = []
        self.characterNameElements = []
        self.characterPasswordElements = []

        self.selectedType = None

        self.backButton = None
        self.backButtonText = "<- Back"

        self.titleFont = pygame.font.Font(GAME_FONT_PATH, TITLE_FONT_SIZE)
        self.labelFont = pygame.font.Font(GAME_FONT_PATH, MED_FONT_SIZE)
        self.regularFont = pygame.font.Font(GAME_FONT_PATH, REG_FONT_SIZE)

        self.characterNameInterfaceShown = False
        self.characterNameReceived = False

        self.initializeBackButton()
        self.initializeCharacterTypeElements()
    #------------------------------#

    #------------------------------#
    # Function that initializes the back button   
    def initializeBackButton(self):
        backButtonTextWidth, backButtonTextHeight = self.titleFont.size(self.backButtonText)
        backButtonTLx = 5
        backButtonTLy = 15
        self.backButton = InteractiveRect(backButtonTLx, backButtonTLy, width=backButtonTextWidth, height=backButtonTextHeight, defaultColor=BLACK, highlightColor=BLACK, defaultTextColor=WHITE, highlightTextColor=BATTLE_TEXT_HIGHLIGHT_COLOR, parentID=self.gameObjectID, text=self.backButtonText, textCoordinates=(backButtonTLx, backButtonTLy), fontSize=TITLE_FONT_SIZE, callbackArg="back")

        # Set a signal listener for the back button
        self.setSignalListener(msg="clicked", sourceID=self.backButton.getGameObjectID(), callback=self.backButtonClicked)
    #------------------------------#

    #------------------------------#
    # Destructor Function   
    def __del__(self):
        if (self.backButton != None):
            self.backButton.__del__()

        for el in self.characterNameElements:
            if el["name"] == "nameTextbox":
                el["textbox"].__del__()
            if el["name"] == "label":
                el["text"].__del__()
        self.characterNameElements = []

        for el in self.characterPasswordElements:
            if el["name"] == "passwordTextbox":
                el["textbox"].__del__()
            if el["name"] == "label":
                el["text"].__del__()
        self.characterPasswordElements = []

        for el in self.characterTypeElements:
            el["rect"].__del__()
            el["sprite"].__del__()
            el["label"].__del__()
        self.characterTypeElements = []

        for el in self.typeConfirmationElements:
            if el["name"] == "confirm" or el["name"] == "cancel":
                el["rect"].__del__()
            elif el["name"] == "character":
                el["sprite"].__del__()
                el["label"].__del__()
                el["rect"].__del__()
            else:
                el["text"].__del__()
        self.typeConfirmationElements = []

        super().__del__()
    #------------------------------#

    #------------------------------#
    # Function that is called when the character name is submitted
    def characterNameSubmitted(self, characterName):
        for el in self.characterNameElements:
            if el["name"] == "nameTextbox":
                el["textbox"].__del__()
            if el["name"] == "label":
                el["text"].__del__()
        self.characterNameElements = []

        character = {
            "name": characterName,
            "type": self.selectedType,
            "inventory": [],
            "HP": 100,
            "maxHealth": 100,
            "abilityUses": 3
        }

        self.character = character
        self.characterNameReceived = True

        self.initializeCharacterPasswordElements()
    #------------------------------#

    #------------------------------#
    # Function that is called when the character's file password is submitted
    def characterPasswordSubmitted(self, password):
        # Call the game engine in an attempt to create the character
        characterCreationStatus = super().attemptCreateCharacter(self.character["name"], password)

        # Delete the UI elements
        for el in self.characterPasswordElements:
            if el["name"] == "passwordTextbox":
                el["textbox"].__del__()
            if el["name"] == "label":
                el["text"].__del__()
        self.characterPasswordElements = []

        # If the character creation was successful, then move on. Otherwise, show the password input again
        if characterCreationStatus:
            self.emitSignal(msg="character-created", data=self.character, targetID=self.parentID)
        else:
            self.initializeCharacterPasswordElements()
    #------------------------------#

    #------------------------------#
    # Function that is called when a character type is selected
    def characterTypeSelected(self, typeName):
        for characterType in self.characterTypes:
            if characterType["name"] == typeName:
                self.selectedType = characterType

        for el in self.characterTypeElements:
            el["rect"].__del__()
            el["sprite"].__del__()
            el["label"].__del__()
        self.characterTypeElements = []

        self.initializeTypeConfirmationElements()
    #------------------------------#

    #------------------------------#
    # Function that is called when a type confirmation option is selected
    def confirmOptionSelected(self, option):
        for el in self.typeConfirmationElements:
            if el["name"] == "confirm" or el["name"] == "cancel":
                el["rect"].__del__()
            elif el["name"] == "character":
                el["sprite"].__del__()
                el["label"].__del__()
                el["rect"].__del__()
            else:
                el["text"].__del__()
        self.typeConfirmationElements = []

        if option == "cancel":
            self.initializeCharacterTypeElements()
        if option == "confirm":
            self.initializeCharacterNameElements()
    #------------------------------#

    #------------------------------#
    # Function that initializes the elements used by the character name input screen
    def initializeCharacterNameElements(self):
        # Initialize the character name textbox and set a signal listener
        _, regularCharHeight = self.regularFont.size("A")
        textboxHeight = regularCharHeight + 8
        characterNameTextbox_TLx = SCREEN_WIDTH//2
        characterNameTextbox_TLy = SCREEN_HEIGHT//2 - textboxHeight//2
        characterNameTextbox = Textbox(characterNameTextbox_TLx, characterNameTextbox_TLy, parentID=self.gameObjectID)

        el = {"name": "nameTextbox", "textbox": characterNameTextbox}
        self.characterNameElements.append(el)

        self.setSignalListener(msg="submitted", sourceID=characterNameTextbox.getGameObjectID(), callback=self.characterNameSubmitted)

        # Initialize the character name textbox label
        characterNameLabelWidth, characterNameLabelHeight = self.labelFont.size("CHARACTER NAME:")
        characterNameLabelTLx = characterNameTextbox_TLx - characterNameLabelWidth - 10
        characterNameLabelTLy = SCREEN_HEIGHT//2 - characterNameLabelHeight//2

        characterNameInputLabel = SimpleText("CHARACTER NAME:", fontSize=MED_FONT_SIZE, x=characterNameLabelTLx, y=characterNameLabelTLy)

        labelEl = {"name": "label", "text": characterNameInputLabel}
        self.characterNameElements.append(labelEl)

        self.characterNameInterfaceShown = True
    #------------------------------#

    #------------------------------#
    # Function that initializes the elements used by the character file password input screen
    def initializeCharacterPasswordElements(self):
        _, regularCharHeight = self.regularFont.size("A")
        textboxHeight = regularCharHeight + 8
        characterPasswordTextbox_TLx = SCREEN_WIDTH//2
        characterPasswordTextbox_TLy = SCREEN_HEIGHT//2 - textboxHeight//2
        characterPasswordTextbox = Textbox(characterPasswordTextbox_TLx, characterPasswordTextbox_TLy, parentID=self.gameObjectID)

        el = {"name": "passwordTextbox", "textbox": characterPasswordTextbox}
        self.characterPasswordElements.append(el)

        characterPasswordTextboxID = characterPasswordTextbox.getGameObjectID()
        self.setSignalListener(msg="submitted", sourceID=characterPasswordTextboxID, callback=self.characterPasswordSubmitted)

        characterPasswordLabelWidth, characterPasswordLabelHeight = self.labelFont.size("PASSWORD:")
        characterPasswordLabelTLx = characterPasswordTextbox_TLx - characterPasswordLabelWidth - 10
        characterPasswordLabelTLy = SCREEN_HEIGHT//2 - characterPasswordLabelHeight//2

        characterPasswordInputLabel = SimpleText("PASSWORD:", fontSize=MED_FONT_SIZE, x=characterPasswordLabelTLx, y=characterPasswordLabelTLy)

        labelEl = {"name": "label", "text": characterPasswordInputLabel}
        self.characterPasswordElements.append(labelEl)
    #------------------------------#

    #------------------------------#
    # Function that initializes the elements used in the character type selector
    def initializeCharacterTypeElements(self):
        medianIndex = math.ceil(len(self.characterTypes) / 2) - 1
        for index, type in enumerate(self.characterTypes):
            rect_TLx = SCREEN_WIDTH//2 - 50 - ((medianIndex-index) * 110)
            rect_TLy = SCREEN_HEIGHT//2 - 50

            characterRect = InteractiveRect(rect_TLx, rect_TLy, 100, 100, outlineOnly=True, defaultColor=WHITE, highlightColor=BLUE, text=None, callbackArg=type["name"], parentID=self.gameObjectID,)

            sprite = AnimatedSprite("Assets", type["animations"], centerX=rect_TLx + 50, centerY=rect_TLy + 50)

            characterRectID = characterRect.getGameObjectID()
            self.setSignalListener(msg="clicked", sourceID=characterRectID, callback=self.characterTypeSelected)

            characterLabel = SimpleText(type["name"], x=rect_TLx+50, y=rect_TLy+112, behavior="center")

            el = {"name": type["name"], "rect": characterRect, "sprite": sprite, "label": characterLabel}
            self.characterTypeElements.append(el)
    #------------------------------#

    #------------------------------#
    # Function that initializes the elements used in the character type confirmation screen
    def initializeTypeConfirmationElements(self):
        self.typeConfirmationElements = []

        # Render the confirm and cancel buttons
        confirmTextWidth, confirmTextHeight = self.regularFont.size("Confirm")
        cancelTextWidth, cancelTextHeight = self.regularFont.size("Cancel")

        confirm_rect_TLx = SCREEN_WIDTH//2 - (confirmTextWidth+5) - 3
        confirm_rect_TLy = SCREEN_HEIGHT - 100
        confirmRect = InteractiveRect(confirm_rect_TLx, confirm_rect_TLy, confirmTextWidth + 5, confirmTextHeight + 6, defaultColor=BLACK, highlightColor=WHITE, defaultTextColor=WHITE, highlightTextColor=BLACK, text="Confirm", textCoordinates=(confirm_rect_TLx + 3, confirm_rect_TLy + 3), callbackArg="confirm", parentID=self.gameObjectID)

        confirmElement = {"name": "confirm", "rect": confirmRect}
        self.typeConfirmationElements.append(confirmElement)

        confirmRectID = confirmRect.getGameObjectID()
        self.setSignalListener(msg="clicked", sourceID=confirmRectID, callback=self.confirmOptionSelected)

        cancel_rect_TLx = SCREEN_WIDTH//2 + 3
        cancel_rect_TLy = SCREEN_HEIGHT - 100
        cancelRect = InteractiveRect(cancel_rect_TLx, cancel_rect_TLy, cancelTextWidth + 5, cancelTextHeight + 6, defaultColor=BLACK, highlightColor=WHITE, defaultTextColor=WHITE, highlightTextColor=BLACK, text="Cancel", textCoordinates=(cancel_rect_TLx + 3, cancel_rect_TLy + 3), callbackArg="cancel", parentID=self.gameObjectID)

        cancelElement = {"name": "cancel", "rect": cancelRect}
        self.typeConfirmationElements.append(cancelElement)

        cancelRectID = cancelRect.getGameObjectID()
        self.setSignalListener(msg="clicked", sourceID=cancelRectID, callback=self.confirmOptionSelected)

        # Render the character sprite and its border rectangle
        characterDisplayRect_TLx = SCREEN_WIDTH//2 - 50
        characterDisplayRect_TLy = 50
        characterDisplayRect = InteractiveRect(characterDisplayRect_TLx, characterDisplayRect_TLy, 100, 100, outlineOnly=True, defaultColor=WHITE, highlightColor=WHITE, text=None)
        
        characterSprite = AnimatedSprite("Assets", self.selectedType["animations"], centerX=characterDisplayRect_TLx + 50, centerY=characterDisplayRect_TLy + 50)

        characterLabel = SimpleText(self.selectedType["name"], x=characterDisplayRect_TLx+50, y=characterDisplayRect_TLy+112, behavior="center")

        characterElement = {"name": "character", "sprite": characterSprite, "rect": characterDisplayRect, "label": characterLabel}
        self.typeConfirmationElements.append(characterElement)

        # Render the character description and its accompanying label
        descriptionLabel = SimpleText("Description: ", TITLE_FONT_SIZE, x=SCREEN_WIDTH//2-250, y=characterDisplayRect_TLy + 200)
        descriptionElement = {"name": "description-label", "text": descriptionLabel}
        self.typeConfirmationElements.append(descriptionElement)

        characterDescriptionParts = prepareTextForRendering(self.selectedType["description"], REG_FONT_SIZE, 500)

        for index, descriptionPart in enumerate(characterDescriptionParts):
            _, descriptionTextHeight = self.regularFont.size(descriptionPart)

            descriptionText = SimpleText(descriptionPart, x=SCREEN_WIDTH//2-250, y=characterDisplayRect_TLy + 250 + ((5 + descriptionTextHeight) * index))
            textElement = {"name": "description-" + str(index), "text": descriptionText}
            self.typeConfirmationElements.append(textElement)
    #------------------------------#

    #------------------------------#
    # Function that is called when the back button is clicked       
    def backButtonClicked(self, _):
        if self.selectedType == None:
            self.emitSignal(msg="close-character-creator", data=None, targetID=self.parentID)
        elif self.selectedType != None and (not self.characterNameInterfaceShown):
            self.selectedType = None
            self.confirmOptionSelected("cancel")
        elif self.characterNameInterfaceShown and (not self.characterNameReceived):
            for el in self.characterNameElements:
                if el["name"] == "nameTextbox":
                    el["textbox"].__del__()
                if el["name"] == "label":
                    el["text"].__del__()
            self.characterTypeSelected(self.selectedType["name"])
            self.characterNameInterfaceShown = False
        elif self.characterNameInterfaceShown and self.characterNameReceived:
            for el in self.characterPasswordElements:
                if el["name"] == "passwordTextbox":
                    el["textbox"].__del__()
                if el["name"] == "label":
                    el["text"].__del__()
            self.characterPasswordElements = []
            self.characterNameReceived = False
            self.initializeCharacterNameElements()
    #------------------------------#
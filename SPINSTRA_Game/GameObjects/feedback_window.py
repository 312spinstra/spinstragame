import pygame
from .game_object import GameObject
from .interactive_rect import InteractiveRect
from .simple_text import SimpleText
from constants import *
from utils import *

# Class that implements the Feedback Window
class FeedbackWindow(GameObject):
    #------------------------------#
    # Constructor Function
    def __init__(self, title="", feedback="", centerX=SCREEN_WIDTH//2, centerY=SCREEN_HEIGHT//2-100, width=500, height=300, backgroundColor=BATTLE_OPTIONS_BACKGROUND_COLOR, borderColor=WHITE, parentID="", zIndex=10):
        super().__init__(zIndex=zIndex)
        self.parentID = parentID
        self.titleText = title
        self.feedbackText = feedback
        self.centerX = centerX
        self.centerY = centerY
        self.width = width
        self.height = height
        self.TLx = self.centerX - self.width//2
        self.TLy = self.centerY - height//2
        self.backgroundColor = backgroundColor
        self.borderColor = borderColor
        self.closeButton = None
        self.feedbackTextParts = []
        self.feedbackParts = []
        self.title = None
        self.titleFont = pygame.font.Font(GAME_FONT_PATH, MED_FONT_SIZE)
        self.feedbackFont = pygame.font.Font(GAME_FONT_PATH, REG_FONT_SIZE)
        self.initializeElements()
    #------------------------------#

    #------------------------------#
    # Destructor Function
    def __del__(self):
        for part in self.feedbackParts:
            part.__del__()
        self.title.__del__()
        self.closeButton.__del__()
        super().__del__()
    #------------------------------#

    #------------------------------#
    # Function that initializes all the UI elements
    def initializeElements(self):
        # Initialize the close button and set a signal listener
        closeButtonFont = pygame.font.Font(GAME_FONT_PATH, TITLE_FONT_SIZE)
        closeButtonTextWidth, closeButtonTextHeight = closeButtonFont.size("X")
        closeButtonTLx = self.TLx + self.width - closeButtonTextWidth - 5
        closeButtonTLy = self.TLy + 5

        self.closeButton = InteractiveRect(closeButtonTLx, closeButtonTLy, closeButtonTextWidth, closeButtonTextHeight, defaultColor=self.backgroundColor, highlightColor=self.backgroundColor, defaultTextColor=WHITE, highlightTextColor=BATTLE_TEXT_HIGHLIGHT_COLOR, fontSize=MED_FONT_SIZE, text="X", textCoordinates=(closeButtonTLx, closeButtonTLy), parentID=self.gameObjectID, callbackArg=True, zIndex=self.zIndex + 1)

        self.setSignalListener(msg="clicked", sourceID=self.closeButton.getGameObjectID(), callback=self.closeButtonClicked)

        # Initialize the title
        titleTLx = self.TLx + 5
        titleTLy = self.TLy + 5
        _, titleTextHeight = self.titleFont.size(self.titleText)

        self.title = SimpleText(self.titleText, x=titleTLx, y =titleTLy, fontSize=MED_FONT_SIZE, zIndex=self.zIndex+1)

        # Initialize the feedback parts
        self.feedbackTextParts = prepareTextForRendering(self.feedbackText, REG_FONT_SIZE, self.width-10)

        _, textHeight = self.feedbackFont.size(self.feedbackText)

        textTLx = self.TLx + 5
        textStartingTLy = self.TLy + titleTextHeight + 15

        for index, part in enumerate(self.feedbackTextParts):
            feedbackPart = SimpleText(part, x=textTLx, y = textStartingTLy + ((5 + textHeight) * index), fontSize=REG_FONT_SIZE, zIndex=self.zIndex+1)
            self.feedbackParts.append(feedbackPart)
    #------------------------------#

    #------------------------------#
    # Function that renders the item info windows
    def render(self, canvas):
        # Render the background and border rectangles
        backgroundRect = pygame.Rect(self.TLx, self.TLy, self.width, self.height)
        borderRect = pygame.Rect(self.TLx, self.TLy, self.width, self.height)

        pygame.draw.rect(canvas, self.backgroundColor, backgroundRect)
        pygame.draw.rect(canvas, self.borderColor, borderRect, 2)
    #------------------------------#

    #------------------------------#
    # Function that is called when the close button is clicked
    def closeButtonClicked(self, _):
        self.emitSignal(msg="close", data=None, targetID=self.parentID)
    #------------------------------#

import pygame
from .game_object import GameObject
from .interactive_rect import InteractiveRect
from .textarea import Textarea
from .simple_text import SimpleText
from constants import *
from utils import *

# Class that implements the Question Modal
class QuestionModal(GameObject):
    #------------------------------#
    # Constructor Function
    def __init__(self, centerX, centerY, width, height, question, answer, questionInfo, zIndex=10, parentID=""):
        super().__init__(zIndex=zIndex)
        self.centerX = centerX
        self.centerY = centerY
        self.width = width
        self.height = height
        self.TLx = self.centerX - self.width//2
        self.TLy = self.centerY - self.height//2
        self.question = question
        self.questionParts = None
        self.answer = answer
        self.questionInfo = questionInfo
        self.parentID = parentID
        self.answerTextbox = None
        self.textParts = []

        self.initializeElements()
    #------------------------------#

    #------------------------------#
    # Destructor Function
    def __del__(self):
        for part in self.textParts:
            part.__del__()

        self.answerTextbox.__del__()
        self.closeButton.__del__()

        super().__del__()
    #------------------------------#

    #------------------------------#
    # Function that initializes the elements used by the modal
    def initializeElements(self):
        # Initialize the answer textarea and set a signal listener
        textboxTLx = self.centerX - self.width//2 + 10
        textboxTLy = self.centerY + self.height//2 - 140
        textboxWidth = self.width - 20
        modalZIndex = self.getZIndex()

        self.answerTextbox = Textarea(textboxTLx, textboxTLy, textboxWidth, 130, parentID=self.gameObjectID, zIndex=modalZIndex + 1) 
        self.setSignalListener(msg="submitted", sourceID=self.answerTextbox.getGameObjectID(), callback=self.answerSubmitted)

        # Initialize the close button and set a signal listener
        closeButtonFont = pygame.font.Font(GAME_FONT_PATH, TITLE_FONT_SIZE)
        closeButtonTextWidth, closeButtonTextHeight = closeButtonFont.size("X")
        closeButtonTLx = self.TLx + self.width - closeButtonTextWidth - 5
        closeButtonTLy = self.TLy + 5

        self.closeButton = InteractiveRect(closeButtonTLx, closeButtonTLy, closeButtonTextWidth, closeButtonTextHeight, defaultColor=BATTLE_OPTIONS_BACKGROUND_COLOR, highlightColor=BATTLE_OPTIONS_BACKGROUND_COLOR, defaultTextColor=WHITE, highlightTextColor=BATTLE_TEXT_HIGHLIGHT_COLOR, fontSize=MED_FONT_SIZE, text="X", textCoordinates=(closeButtonTLx, closeButtonTLy), parentID=self.gameObjectID, callbackArg=True, zIndex=modalZIndex + 1)

        closeButtonID = self.closeButton.getGameObjectID()
        self.setSignalListener(msg="clicked", sourceID=closeButtonID, callback=self.closeButtonClicked)

        # Initialize the question text parts
        self.questionParts = prepareTextForRendering(self.question, REG_FONT_SIZE, self.width-20)

        questionTLx = self.TLx + 10
        questionTLy = self.TLy + 30

        questionFont = pygame.font.Font(GAME_FONT_PATH, REG_FONT_SIZE)
        _, textHeight = questionFont.size(self.question)

        for index, part in enumerate(self.questionParts):
            partText = SimpleText(text=part, x=questionTLx, y=questionTLy + ((5 + textHeight) * index), zIndex=modalZIndex+1)
            self.textParts.append(partText)
    #------------------------------#

    #------------------------------#
    # Function that renders the question modal on the canvas
    def render(self, canvas):
        backgroundRect = pygame.Rect(self.TLx, self.TLy, self.width, self.height)
        borderRect = pygame.Rect(self.TLx, self.TLy, self.width, self.height)

        pygame.draw.rect(canvas, BATTLE_OPTIONS_BACKGROUND_COLOR, backgroundRect)
        pygame.draw.rect(canvas, WHITE, borderRect, 2)
    #------------------------------#

    #------------------------------#
    # Function that is called when an answer is submitted
    def answerSubmitted(self, userAnswer):
        answerIsCorrect = checkAnswer(userAnswer, self.questionInfo)
        self.emitSignal(msg="result-determined", data=answerIsCorrect, targetID=self.parentID)
    #------------------------------#

    #------------------------------#
    # Function that is called when the close button is clicked
    def closeButtonClicked(self, _):
        self.emitSignal(msg="close-modal", data=True, targetID=self.parentID)
    #------------------------------#

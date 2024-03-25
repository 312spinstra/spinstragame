import pygame
import random
from .game_object import GameObject
from .interactive_rect import InteractiveRect
from .textarea import Textarea
from .simple_text import SimpleText
from .multiple_choice_option import MultipleChoiceOption
from constants import *
from utils import *

# Class that implements the Multiple Choice Question Modal
class MultipleChoiceQuestionModal(GameObject):
    #------------------------------#
    # Constructor Function
    def __init__(self, centerX, centerY, width, height, question, answer, questionInfo, incorrectAnswers, zIndex=10, parentID=""):
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
        self.incorrectAnswers = incorrectAnswers
        self.orderedOptions = []
        self.parentID = parentID
        self.textParts = []
        self.multipleChoiceOptions = []
        self.selectedOption = None
        self.submitButton = None
        self.orderOptions()
        self.initializeElements()
    #------------------------------#

    #------------------------------#
    # Destructor Function
    def __del__(self):
        for part in self.textParts:
            part.__del__()

        for option in self.multipleChoiceOptions:
            option["el"].__del__()

        self.closeButton.__del__()
        self.submitButton.__del__()

        super().__del__()
    #------------------------------#

    #------------------------------#
    # Function that initializes the elements used by the modal
    def initializeElements(self):
        # Get the zIndex of the background
        modalZIndex = self.getZIndex()

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

        partTextTLy = 0
        for index, part in enumerate(self.questionParts):
            partTextTLy = questionTLy + ((5 + textHeight) * index)
            partText = SimpleText(text=part, x=questionTLx, y=partTextTLy, zIndex=modalZIndex+1)
            self.textParts.append(partText)

        initialOptionTLy = partTextTLy + 10
        lastOptionTLy = initialOptionTLy

        # Initialize the multiple choice options and set signal listeners
        regFont = pygame.font.Font(GAME_FONT_PATH, REG_FONT_SIZE)
        for index, option in enumerate(self.orderedOptions):
            _, optionTextHeight = regFont.size(option)
            optionTLy = lastOptionTLy + optionTextHeight + 15
            lastOptionTLy = optionTLy

            multiple_choice_option = MultipleChoiceOption(questionTLx, optionTLy, option, zIndex=modalZIndex+1, parentID=self.gameObjectID)
            choice = {"option": option, "el": multiple_choice_option}
            self.multipleChoiceOptions.append(choice)

            optionID = multiple_choice_option.getGameObjectID()
            self.setSignalListener(msg="option-selected", sourceID=optionID, callback=self.optionSelected)
            self.setSignalListener(msg="option-deselected", sourceID=optionID, callback=self.optionDeselected)

        # Initialize the submit button and set a signal listener
        medFont = pygame.font.Font(GAME_FONT_PATH, MED_FONT_SIZE)
        submitButtonText = "Submit"
        submitButtonTextWidth, submitButtonTextHeight = medFont.size(submitButtonText)
        submitButtonTLx = self.TLx + self.width//2 - submitButtonTextWidth//2
        submitButtonTLy = self.TLy + self.height - submitButtonTextHeight - 30
        
        self.submitButton = InteractiveRect(submitButtonTLx, submitButtonTLy, width=submitButtonTextWidth + 10, height=submitButtonTextHeight + 10, defaultColor=BATTLE_OPTIONS_BACKGROUND_COLOR, highlightColor=WHITE, defaultTextColor=WHITE, highlightTextColor=BATTLE_OPTIONS_BACKGROUND_COLOR, text=submitButtonText, textCoordinates=(submitButtonTLx + 5, submitButtonTLy + 5), fontSize=MED_FONT_SIZE, zIndex=modalZIndex+1, parentID=self.gameObjectID)

        self.setSignalListener(msg="clicked", sourceID=self.submitButton.getGameObjectID(), callback=self.submitButtonClicked)
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
    # Function that is called when the close button is clicked
    def closeButtonClicked(self, _):
        self.emitSignal(msg="close-modal", data=True, targetID=self.parentID)
    #------------------------------#

    #------------------------------#
    # Function that determines the order and placement of the correct option in the list of options   
    def orderOptions(self):
        # Select a random index for the correct answer
        correctOptionIndex = random.randrange(len(self.incorrectAnswers))

        # Combine the correct and incorrect answers into a list in the appropriate order
        for i in range(len(self.incorrectAnswers) + 1):
            if (i == correctOptionIndex):
                self.orderedOptions.append(self.answer)
            else:
                incorrectAnswer = self.incorrectAnswers.pop(0)
                self.orderedOptions.append(incorrectAnswer)
    #------------------------------#

    #------------------------------#
    # Function that is called when an option is selected           
    def optionSelected(self, option):
        if self.selectedOption != None:
            for choice in self.multipleChoiceOptions:
                if choice["option"] == self.selectedOption:
                    choice["el"].deselect()
                    break

        self.selectedOption = option
    #------------------------------#

    #------------------------------#
    # Function that is called when the selected option is manually deselected
    def optionDeselected(self, option):
        self.selectedOption = None
    #------------------------------#

    #------------------------------#
    # Function that is called when the submit button is clicked 
    def submitButtonClicked(self, _):
        if self.selectedOption != None:
            answerIsCorrect = checkAnswer(self.selectedOption, self.questionInfo)
            self.emitSignal(msg="result-determined", data=answerIsCorrect, targetID=self.parentID)
    #------------------------------#
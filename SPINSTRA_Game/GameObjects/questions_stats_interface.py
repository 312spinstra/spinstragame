import pygame
from .game_object import GameObject
from .simple_text import SimpleText
from .interactive_rect import InteractiveRect
from constants import *

# Class that implements the Question Stats Interface
class QuestionStatsInterface(GameObject):
    #------------------------------#
    # Constructor Function
    def __init__(self, parentID=""):
        super().__init__()
        self.parentID = parentID
        self.titleFont = pygame.font.Font(GAME_FONT_PATH, TITLE_FONT_SIZE)
        self.largeFont = pygame.font.Font(GAME_FONT_PATH, MED_FONT_SIZE)
        self.mediumFont = pygame.font.Font(GAME_FONT_PATH, REG_FONT_SIZE)
        self.questionStats = []
        self.topicSections = []
        self.statRows = []
        self.title = None
        self.titleText = "Question Stats"
        self.backButton = None
        self.backButtonText = "<- Back"
        self.gameRuntimeDisplay = None
        self.gameRuntimeText = "Runtime: " 
        self.getQuestionStats()
        self.initializeElements()
    #------------------------------#

    #------------------------------#
    # Destructor Function
    def __del__(self):
        self.title.__del__()
        self.backButton.__del__()
        self.gameRuntimeDisplay.__del__()

        for section in self.topicSections:
            for el in section["elements"]:
                el.__del__()
        
        super().__del__()
    #------------------------------#

    #------------------------------#
    # Function that initializes the UI elements used in this interface
    def initializeElements(self):
        # Initialize the interface title
        titleTextWidth, titleTextHeight = self.titleFont.size(self.titleText)
        titleTLx = SCREEN_WIDTH//2 - titleTextWidth//2
        titleTLy = 15
        self.title = SimpleText(text=self.titleText, fontSize=TITLE_FONT_SIZE, x=titleTLx, y=titleTLy)

        # Initialize the back button and set a signal listener
        backButtonTextWidth, backButtonTextHeight = self.titleFont.size(self.backButtonText)
        backButtonTLx = 5
        backButtonTLy = 15
        self.backButton = InteractiveRect(backButtonTLx, backButtonTLy, width=backButtonTextWidth, height=backButtonTextHeight, defaultColor=BLACK, highlightColor=BLACK, defaultTextColor=WHITE, highlightTextColor=BATTLE_TEXT_HIGHLIGHT_COLOR, parentID=self.gameObjectID, text=self.backButtonText, textCoordinates=(backButtonTLx, backButtonTLy), fontSize=TITLE_FONT_SIZE, callbackArg="back")

        self.setSignalListener(msg="clicked", sourceID=self.backButton.getGameObjectID(), callback=self.backButtonClicked)

        # Initialize the game runtime display text
        self.gameRuntimeText = self.gameRuntimeText + self.getGameRuntime()
        gameRuntimeTextWidth, _ = self.largeFont.size(self.gameRuntimeText)
        gameRuntimeDisplayTLx = SCREEN_WIDTH - gameRuntimeTextWidth - 10
        gameRuntimeDisplayTLy = 15
        self.gameRuntimeDisplay = SimpleText(text=self.gameRuntimeText, fontSize=MED_FONT_SIZE, x=gameRuntimeDisplayTLx, y=gameRuntimeDisplayTLy)

        # Group the question stats groups into sets of 5
        for i in range(0, len(self.questionStats), 5):
            self.statRows.append(self.questionStats[i: i + 5])

        # Initialize the sections for each of the topics
        for rowIndex, row in enumerate(self.statRows):
            for colIndex, stat in enumerate(row):
                topic = stat["topic"]
                correctCount = stat["correct"]
                incorrectCount = stat["incorrect"]
                totalQuestionsCount = correctCount + incorrectCount
                if (totalQuestionsCount > 0):
                    percentage = round((correctCount/totalQuestionsCount) * 100)
                else:
                    percentage = 100

                topicSection = {"topic": topic, "elements": []}

                topicTitle = topic.capitalize() + " - (" + str(percentage) + "%)"
                correctText = "Correct: " + str(correctCount)
                incorrectText = "Incorrect: " + str(incorrectCount)
                dividerLine = "--------------------"
                totalText = "Total: " + str(totalQuestionsCount)

                topicTitleWidth, topicTitleHeight = self.largeFont.size(topicTitle)
                correctTextWidth, correctTextHeight = self.mediumFont.size(correctText)
                incorrectTextWidth, incorrectTextHeight = self.mediumFont.size(incorrectText)
                dividerLineWidth, dividerLineHeight = self.mediumFont.size(dividerLine)

                topicTitleTLx = 15 + (colIndex * 180) + (colIndex * 150)
                topicTitleTLy = 75 + (rowIndex * 250)

                topicTitleTextDisplay = SimpleText(text=topicTitle, fontSize=MED_FONT_SIZE, x=topicTitleTLx, y=topicTitleTLy)
                topicSection["elements"].append(topicTitleTextDisplay)

                correctTextTLx = topicTitleTLx
                correctTextTLy = topicTitleTLy + topicTitleHeight + 10

                correctTextDisplay = SimpleText(text=correctText, fontSize=REG_FONT_SIZE, x=correctTextTLx, y=correctTextTLy)
                topicSection["elements"].append(correctTextDisplay)

                incorrectTextTLx = topicTitleTLx
                incorrectTextTLy = correctTextTLy + correctTextHeight + 5

                incorrectTextDisplay = SimpleText(text=incorrectText, fontSize=REG_FONT_SIZE, x=incorrectTextTLx, y=incorrectTextTLy)
                topicSection["elements"].append(incorrectTextDisplay)

                dividerLineTLx = topicTitleTLx
                dividerLineTLy = incorrectTextTLy + incorrectTextHeight + 5

                dividerLineDisplay = SimpleText(text=dividerLine, fontSize=REG_FONT_SIZE, x=dividerLineTLx, y=dividerLineTLy)
                topicSection["elements"].append(dividerLineDisplay)

                totalTextTLx = topicTitleTLx
                totalTextTLy = dividerLineTLy + dividerLineHeight + 5

                totalTextDisplay = SimpleText(text=totalText, fontSize=REG_FONT_SIZE, x=totalTextTLx, y=totalTextTLy)
                topicSection["elements"].append(totalTextDisplay)

                self.topicSections.append(topicSection)
    #------------------------------#

    #------------------------------#
    # Function that gets the question stats from the Game Engine  
    def getQuestionStats(self):
        self.questionStats = self.getGlobalDictValue("questionStats")
    #------------------------------#

    #------------------------------#
    # Function that returns the Game Object IDs of the UI elements
    def getElementIDs(self):
        ids = []
        ids.append(self.title.getGameObjectID())
        ids.append(self.backButton.getGameObjectID())
        ids.append(self.gameRuntimeDisplay.getGameObjectID())
        for section in self.topicSections:
            for el in section["elements"]:
                ids.append(el.getGameObjectID())
        return ids
    #------------------------------#

    #------------------------------#
    # Function that is called when the "back" button is clicked
    def backButtonClicked(self, _):
        self.emitSignal(msg="close-stats-menu", data=None, targetID=self.parentID)
    #------------------------------#
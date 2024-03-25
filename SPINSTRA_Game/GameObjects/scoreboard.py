import pygame
from .game_object import GameObject
from .simple_text import SimpleText
from .interactive_rect import InteractiveRect
from constants import *
from utils import loadCSVFile

# Class that implements the Scoreboard
class Scoreboard(GameObject):
    #------------------------------#
    # Constructor Function
    def __init__(self, parentID=""):
        super().__init__()
        self.parentID = parentID
        self.largeFont = pygame.font.Font(GAME_FONT_PATH, TITLE_FONT_SIZE)
        self.mediumFont = pygame.font.Font(GAME_FONT_PATH, MED_FONT_SIZE)
        self.numScoresShown = 20
        self.scores = []
        self.scoreElements = []
        self.columnTitleElements = []
        self.title = None
        self.titleText = "Scoreboard"
        self.backButton = None
        self.backButtonText = "<- Back"
        self.getScores()
        self.initializeElements()
    #------------------------------#

    #------------------------------#
    # Destructor Function
    def __del__(self):
        self.title.__del__()
        self.backButton.__del__()

        for el in self.columnTitleElements:
            el.__del__()

        for el in self.scoreElements:
            el.__del__()
        
        super().__del__()
    #------------------------------#

    #------------------------------#
    # Function that initializes the UI elements used in this interface
    def initializeElements(self):
        # Initialize the interface title
        titleTextWidth, titleTextHeight = self.largeFont.size(self.titleText)
        titleTLx = SCREEN_WIDTH//2 - titleTextWidth//2
        titleTLy = 15
        self.title = SimpleText(text=self.titleText, fontSize=TITLE_FONT_SIZE, x=titleTLx, y=titleTLy)

        # Initialize the back button and set a signal listener
        backButtonTextWidth, backButtonTextHeight = self.largeFont.size(self.backButtonText)
        backButtonTLx = 5
        backButtonTLy = 15
        self.backButton = InteractiveRect(backButtonTLx, backButtonTLy, width=backButtonTextWidth, height=backButtonTextHeight, defaultColor=BLACK, highlightColor=BLACK, defaultTextColor=WHITE, highlightTextColor=BATTLE_TEXT_HIGHLIGHT_COLOR, parentID=self.gameObjectID, text=self.backButtonText, textCoordinates=(backButtonTLx, backButtonTLy), fontSize=TITLE_FONT_SIZE, callbackArg="back")

        self.setSignalListener(msg="clicked", sourceID=self.backButton.getGameObjectID(), callback=self.backButtonClicked)

        # Initialize the column titles
        nameColumnTitleText = "Name"
        nameColumnTextWidth, _ = self.largeFont.size(nameColumnTitleText)
        nameColumnTitleTLx = 200 - nameColumnTextWidth//2
        nameColumnTitleTLy = 75
        nameColumnTitle = SimpleText(text=nameColumnTitleText, fontSize=TITLE_FONT_SIZE, x=nameColumnTitleTLx, y=nameColumnTitleTLy)
        self.columnTitleElements.append(nameColumnTitle)

        scoreColumnTitleText = "Score"
        scoreColumnTextWidth, _ = self.largeFont.size(scoreColumnTitleText)
        scoreColumnTitleTLx = SCREEN_WIDTH//2 - scoreColumnTextWidth//2
        scoreColumnTitleTLy = 75
        scoreColumnTitle = SimpleText(text=scoreColumnTitleText, fontSize=TITLE_FONT_SIZE, x=scoreColumnTitleTLx, y=scoreColumnTitleTLy)
        self.columnTitleElements.append(scoreColumnTitle)

        timeColumnTitleText = "Time"
        timeColumnTextWidth, _ = self.largeFont.size(timeColumnTitleText)
        timeColumnTitleTLx = 1200 - timeColumnTextWidth//2
        timeColumnTitleTLy = 75
        timeColumnTitle = SimpleText(text=timeColumnTitleText, fontSize=TITLE_FONT_SIZE, x=timeColumnTitleTLx, y=timeColumnTitleTLy)
        self.columnTitleElements.append(timeColumnTitle)

        # Initialize the elements that will be used to display the scores
        lastRowTLy = 75 + 50
        rowPaddingY = 15
        for (index, score) in enumerate(self.scores):
            if (index > 0):
                rowTLy = lastRowTLy + rowPaddingY
            else:
                rowTLy = lastRowTLy

            nameText = score["Name"]
            nameTextWidth, _ = self.mediumFont.size(nameText)
            nameTextTLx = 200 - nameTextWidth//2
            name = SimpleText(text=nameText, fontSize=MED_FONT_SIZE, x=nameTextTLx, y=rowTLy)
            self.scoreElements.append(name)

            scoreText = score["Score"]
            scoreTextWidth, _ = self.mediumFont.size(scoreText)
            scoreTextTLx = SCREEN_WIDTH//2 - scoreTextWidth//2
            scoreEl = SimpleText(text=scoreText, fontSize=MED_FONT_SIZE, x=scoreTextTLx, y=rowTLy)
            self.scoreElements.append(scoreEl)

            timeText = score["Time"]
            timeTextWidth, timeTextHeight = self.mediumFont.size(timeText)
            timeTextTLx = 1200 - timeTextWidth//2
            time = SimpleText(text=timeText, fontSize=MED_FONT_SIZE, x=timeTextTLx, y=rowTLy)
            self.scoreElements.append(time)

            lastRowTLy = rowTLy + timeTextHeight
    #------------------------------#

    #------------------------------#
    # Function that gets the scores from the local scoreboard 
    def getScores(self):
        # Load the scores from the CSV file
        self.scores = loadCSVFile(SCOREBOARD_FILEPATH)

        # Sort the scores in descending order
        self.scores.sort(key=self.scoreSorting, reverse=True)

        # Only get the top "numScoresShown" scores
        self.scores = self.scores[:self.numScoresShown]
    #------------------------------#

    #------------------------------#
    # Sorting callback that returns an integer version of the user's score
    def scoreSorting(self, val):
        return int(val["Score"])
    #------------------------------#

    #------------------------------#
    # Function that returns the Game Object IDs of the UI elements
    def getElementIDs(self):
        ids = []
        ids.append(self.title.getGameObjectID())
        ids.append(self.backButton.getGameObjectID())
        for el in self.columnTitleElements:
            ids.append(el.getGameObjectID())
        for el in self.scoreElements:
            ids.append(el.getGameObjectID())
        return ids
    #------------------------------#

    #------------------------------#
    # Function that is called when the "back" button is clicked
    def backButtonClicked(self, _):
        self.emitSignal(msg="close-scoreboard", data=None, targetID=self.parentID)
    #------------------------------#
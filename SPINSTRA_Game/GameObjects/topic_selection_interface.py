import pygame
import os
from .game_object import GameObject
from .interactive_rect import InteractiveRect
from .simple_text import SimpleText
from constants import *

# Class that implements the Topic Selection Interface
class TopicSelectionInterface(GameObject):
    #------------------------------#
    # Constructor Function
    def __init__(self, zIndex=0, parentID="", selectedTopics=[]):
        super().__init__(zIndex=zIndex)
        self.parentID = parentID
        self.topics = []
        self.title = None
        self.titleText = "Topic Selection"
        self.subtitle = None
        self.subtitleText = "(Select all topics you would like to review)"
        self.topicButtons = []
        self.submitButton = None
        self.selectedTopics = selectedTopics
        self.titleFont = pygame.font.Font(GAME_FONT_PATH, TITLE_FONT_SIZE)
        self.mediumFont = pygame.font.Font(GAME_FONT_PATH, MED_FONT_SIZE)
        self.getListOfTopics()
        self.initializeElements()
    #------------------------------#
        
    #------------------------------#
    # Destructor Function
    def __del__(self):
        self.title.__del__()
        self.subtitle.__del__()
        self.submitButton.__del__()
        
        for el in self.topicButtons:
            el["button"].__del__()

        super().__del__()
    #------------------------------#

    #------------------------------#
    # Function that gets the list of topics from the application's "Data" folder
    def getListOfTopics(self):
        # Get a list of the subdirectories in the questions directory
        subdirectories = [x[0] for x in os.walk(QUESTIONS_DIRPATH)]

        # Check each subdirectory to ensure it contains a "questions.csv" file
        for subdir in subdirectories:
            questionsFilepath = subdir + "/questions.csv"
            # If the questions file is present, add the subdirectory title to the list of topics
            if (os.path.exists(questionsFilepath) and os.path.isfile(questionsFilepath)):
                path_parts = subdir.split("/")
                topic = path_parts[len(path_parts) - 1]
                self.topics.append(topic)
    #------------------------------#

    #------------------------------#
    # Function that initialize all of the UI elements used in this interface
    def initializeElements(self):
        # Initialize the interface title
        titleTextWidth, titleTextHeight = self.titleFont.size(self.titleText)
        titleTLx = SCREEN_WIDTH//2 - titleTextWidth//2
        titleTLy = 15
        self.title = SimpleText(text=self.titleText, fontSize=TITLE_FONT_SIZE, x=titleTLx, y=titleTLy)

        # Initialize the interface subtitle
        subtitleTextWidth, subtitleTextHeight = self.mediumFont.size(self.subtitleText)
        subtitleTLx = SCREEN_WIDTH//2 - subtitleTextWidth//2
        subtitleTLy = titleTLy + titleTextHeight + 10
        self.subtitle = SimpleText(text=self.subtitleText, fontSize=MED_FONT_SIZE, x=subtitleTLx, y=subtitleTLy)

        # Intialize the submit button and set a signal listener
        submitButtonText = "Submit"
        submitButtonTextWidth, submitButtonTextHeight = self.mediumFont.size(submitButtonText)

        submitButtonTLx = SCREEN_WIDTH//2 - submitButtonTextWidth//2 - 8
        submitButtonTLy = SCREEN_HEIGHT - 50 - submitButtonTextHeight - 8

        submitButtonTextTLx = submitButtonTLx + 8
        submitButtonTextTLy = submitButtonTLy + 8

        self.submitButton = InteractiveRect(TLx=submitButtonTLx, TLy=submitButtonTLy, width=submitButtonTextWidth+16, height=submitButtonTextHeight+16, defaultColor=BLACK, highlightColor=WHITE, defaultTextColor=WHITE, highlightTextColor=BLACK, parentID=self.gameObjectID, text=submitButtonText, textCoordinates=(submitButtonTextTLx, submitButtonTextTLy), fontSize=MED_FONT_SIZE)

        self.setSignalListener(msg="clicked", sourceID=self.submitButton.getGameObjectID(), callback=self.submitButtonClicked)

        # Group all the topics into sets of 5
        topicRows = []
        for i in range(0, len(self.topics), 4):
            row = self.topics[i : i + 4]
            topicRows.append(row)

        # Initialize all of the topic buttons and set signal listeners
        initialColumnTLx = 30
        initialColumnTLy = subtitleTLy + subtitleTextHeight + 20
        rightmostPixel = 0

        for rowIndex, row in enumerate(topicRows):
            for colIndex, col in enumerate(row):
                topicTLx = initialColumnTLx
                topicTLy = initialColumnTLy + (30 * (colIndex-1))

                buttonWidth, buttonHeight = self.mediumFont.size(col)
                if (topicTLx + buttonWidth > rightmostPixel):
                    rightmostPixel = topicTLx + buttonWidth

                defaultTextColor = WHITE
                highlightTextColor = BATTLE_TEXT_HIGHLIGHT_COLOR
                if (col in self.selectedTopics):
                    defaultTextColor = BLUE
                    highlightTextColor = LIGHT_BLUE

                topicButton = InteractiveRect(TLx=topicTLx, TLy=topicTLy, width=buttonWidth, height=buttonHeight, defaultColor=BLACK, highlightColor=BLACK, defaultTextColor=defaultTextColor, highlightTextColor=highlightTextColor, parentID=self.gameObjectID, text=col, textCoordinates=(topicTLx, topicTLy), fontSize=MED_FONT_SIZE, callbackArg=col)

                self.setSignalListener(msg='clicked', sourceID=topicButton.getGameObjectID(), callback=self.topicClicked)

                self.topicButtons.append({"topic": col, "button": topicButton})

            initialColumnTLx = rightmostPixel + 50
    #------------------------------#

    #------------------------------#
    # Function that is called when a topic button is clicked      
    def topicClicked(self, topic):
        # Add the topic if it wasn't already in the list
        if (not(topic in self.selectedTopics)):
            self.selectedTopics.append(topic)
            newDefaultTextColor = BLUE
            newHighlightTextColor = LIGHT_BLUE
        else: # If it was already in the list, remove it
            self.selectedTopics.remove(topic)
            newDefaultTextColor = WHITE
            newHighlightTextColor = BATTLE_TEXT_HIGHLIGHT_COLOR

        # Turn topics in the topic list blue whilst leaving the others white
        for el in self.topicButtons:
                if el["topic"] == topic:
                    el["button"].alterTextColors(newDefaultTextColor, newHighlightTextColor)
                    break
    #------------------------------#

    #------------------------------#
    # Function that is called when the "Submit" button is clicked      
    def submitButtonClicked(self, _):
        if (len(self.selectedTopics) > 0):
            self.emitSignal(msg="topics-selected", data=self.selectedTopics, targetID=self.parentID)
    #------------------------------#

    #------------------------------#
    # Function that returns the Game Object IDs of the child UI elements in this interface
    def getElementIDs(self):
        ids = []
        ids.append(self.title.getGameObjectID())
        ids.append(self.subtitle.getGameObjectID())
        ids.append(self.submitButton.getGameObjectID())
        for el in self.topicButtons:
            ids.append(el["button"].getGameObjectID())
        return ids
    #------------------------------#

import pygame
from .game_object import GameObject
from .simple_text import SimpleText
from constants import *

# Class that implements the Game Finished Screen
class GameFinishedScreen(GameObject):
    #------------------------------#
    # Constructor Function
    def __init__(self, parentID=""):
        super().__init__()
        self.parentID = parentID
        self.congratulationsMessage = None
        self.congratulationsText = "Congratulations! You beat the game!"
        self.characterNameLabel = None
        self.characterNameText = "Character: "
        self.scoreLabel = None
        self.scoreText = "Score: "
        self.timeLabel = None
        self.timeText = "Time: "
        self.largeFont = pygame.font.Font(GAME_FONT_PATH, TITLE_FONT_SIZE)
        self.characterInfo = None
        self.getCharacterInfo()
        self.initializeElements()
    #------------------------------#

    #------------------------------#
    # Destructor Function
    def __del__(self):
        self.congratulationsMessage.__del__()
        self.characterNameLabel.__del__()
        self.scoreLabel.__del__()
        self.timeLabel.__del__()
        super().__del__()
    #------------------------------#

    #------------------------------#
    # Function that initializes the UI elements used in this screen
    def initializeElements(self):
        # Initialize the congratulations message
        congratulationsTextWidth, congratulationsTextHeight = self.largeFont.size(self.congratulationsText)
        congratulationsTLx = SCREEN_WIDTH//2 - congratulationsTextWidth//2
        congratulationsTLy = 15
        self.congratulationsMessage = SimpleText(text=self.congratulationsText, fontSize=TITLE_FONT_SIZE, x=congratulationsTLx, y=congratulationsTLy)
        
        # Intialize the name label
        self.characterNameText += self.characterInfo["name"]
        nameTextWidth, nameTextHeight = self.largeFont.size(self.characterNameText)
        nameLabelTLx = SCREEN_WIDTH//2 - nameTextWidth//2
        nameLabelTLy = congratulationsTLy + congratulationsTextHeight + 50
        self.characterNameLabel = SimpleText(text=self.characterNameText, fontSize=TITLE_FONT_SIZE, x=nameLabelTLx, y=nameLabelTLy)

        # Initialize the score label
        self.scoreText += str(self.characterInfo["score"])
        scoreTextWidth, scoreTextHeight = self.largeFont.size(self.scoreText)
        scoreLabelTLx = SCREEN_WIDTH//2 - scoreTextWidth//2
        scoreLabelTLy = nameLabelTLy + nameTextHeight + 20
        self.scoreLabel = SimpleText(text=self.scoreText, fontSize=TITLE_FONT_SIZE, x=scoreLabelTLx, y=scoreLabelTLy)

        # Initialize the time label
        self.timeText += self.characterInfo["time"]
        timeTextWidth, timeTextHeight = self.largeFont.size(self.timeText)
        timeLabelTLx = SCREEN_WIDTH//2 - timeTextWidth//2
        timeLabelTLy = scoreLabelTLy + scoreTextHeight + 20
        self.timeLabel = SimpleText(text=self.timeText, fontSize=TITLE_FONT_SIZE, x=timeLabelTLx, y=timeLabelTLy)
    #------------------------------#

    #------------------------------#
    # Function that gets the character's info from the Game Engine   
    def getCharacterInfo(self):
        character = self.getGlobalDictValue("character")
        score = self.getGlobalDictValue("userScore")
        runtime = self.getGameRuntime()
        self.characterInfo = {"name": character["name"], "score": score, "time": runtime}
    #------------------------------#
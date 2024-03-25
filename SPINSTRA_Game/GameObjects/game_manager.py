from .game_object import GameObject
from .menu import Menu
from .scoreboard import Scoreboard
from .character_creator import CharacterCreator
from .topic_selection_interface import TopicSelectionInterface
from .main_interface import MainInterface
from .load_game_interface import LoadGameInterface
from engine_initialization import GameEngine
from constants import *
from utils import *

# Class that implements the Game Manager
class GameManager(GameObject):
    #------------------------------#
    # Constructor Function
    def __init__(self):
        super().__init__()
    #------------------------------#
        
    #------------------------------#
    # Function that starts the game
    def begin(self):
        self.showMainMenu()
    #------------------------------#

    #------------------------------#
    # Function that shows the main menu
    def showMainMenu(self):
        self.mainMenu = Menu(MAIN_MENU["title"], MAIN_MENU["options"], parentID=self.gameObjectID)
        self.setSignalListener("option-selected", self.mainMenu.getGameObjectID(), self.handleMainMenuSelection)
    #------------------------------#

    #------------------------------#
    # Function that handles a selection on the main menu
    def handleMainMenuSelection(self, option):
        # Delete the main menu
        self.mainMenu.__del__()

        # Show the appropriate interface based on the user's option
        if option == "Exit":
            GameEngine.quitGame()
        if option == "Continue":
            self.showLoadGameInterface()
        if option == "New Game":
            self.startCharacterCreator()
        if option == "Scoreboard":
            self.showScoreboard()
    #------------------------------#

    #------------------------------#
    # Function that starts up the character creator
    def startCharacterCreator(self):
        # Load in the character types from the JSON file
        characterTypes = loadJSONFile(CHARACTER_TYPES_FILEPATH)

        # Initialize the Character Creator with these character types and set signal listeners
        self.characterCreatorInterface = CharacterCreator(characterTypes, parentID=self.gameObjectID)

        characterCreatorID = self.characterCreatorInterface.getGameObjectID()
        self.setSignalListener(msg="character-created", sourceID=characterCreatorID, callback=self.characterCreated)
        self.setSignalListener(msg="close-character-creator", sourceID=characterCreatorID, callback=self.closeCharacterCreator)
    #------------------------------#

    #------------------------------#
    # Function that is called when character creation is finished
    def characterCreated(self, character):
        self.setGlobalDictValue("character", character)
        
        self.removeSignalListenerBySourceID(self.characterCreatorInterface.getGameObjectID())
        self.characterCreatorInterface.__del__()

        self.initializeNecessaryValues()
        self.startTopicSelectionInterface()
    #------------------------------#

    #------------------------------#
    # Function that initializes values that the main game loop needs in the Game Engine memory
    def initializeNecessaryValues(self):
        # Load the enemy types into the Game Engine memory
        enemyTypes = loadJSONFile(ENEMY_TYPES_FILEPATH)
        self.setGlobalDictValue("enemies", enemyTypes)

        # Load the boss types into the Game Engine memory
        bossTypes = loadJSONFile(BOSS_TYPES_FILEPATH)
        self.setGlobalDictValue("bosses", bossTypes)

        # Load the item types into the Game Engine memory
        itemTypes = loadJSONFile(ITEM_TYPES_FILEPATH)
        for item in itemTypes:
            item["inBattleOnly"] = True if item["inBattleOnly"] == "True" else False
        self.setGlobalDictValue("items", itemTypes)

        # Initialize the Game Engine's seenQuestionIDs collection to empty array
        self.setGlobalDictValue('seenQuestionIDs', [])

        # Initialize the user score to be 0
        self.setGlobalDictValue("userScore", 0)
    #------------------------------#

    #------------------------------#
    # Function that shows the "Load Game" screen and sets up signal listeners
    def showLoadGameInterface(self):
        self.loadGameInterface = LoadGameInterface(parentID=self.gameObjectID)

        loadGameInterfaceID = self.loadGameInterface.getGameObjectID()
        self.setSignalListener(msg="game-loaded", sourceID=loadGameInterfaceID, callback=self.gameLoaded)
        self.setSignalListener(msg="close-load-interface", sourceID=loadGameInterfaceID, callback=self.closeLoadGameInterface)
    #------------------------------#

    #------------------------------#
    # Function that is called whenever the game has been successfully loaded from the "Continue" screen
    def gameLoaded(self, _):
        # Delete the load game interface
        self.removeSignalListenerBySourceID(self.loadGameInterface.getGameObjectID())
        self.loadGameInterface.__del__()

        # Start up the game runtime timer with the initial value of what it was the last time the user was playing
        initialTimerValue = self.getGlobalDictValue("gameRuntime")
        self.startGameTimerInterval(initialTimerValue)

        # Show the Main Game Interface
        self.showMainGameInterface(False)
    #------------------------------#

    #------------------------------#
    # Function that starts up the Topic Selection Interface  
    def startTopicSelectionInterface(self):
        self.topicSelectionInterface = TopicSelectionInterface(parentID=self.gameObjectID)
        self.setSignalListener(msg="topics-selected", sourceID=self.topicSelectionInterface.getGameObjectID(), callback=self.topicsSelected)
    #------------------------------#

    #------------------------------#
    # Function that is called when the user finishes selecting review topics
    def topicsSelected(self, selectedTopics):
        # Delete the Topic Selection Interface
        self.topicSelectionInterface.__del__()

        # Set the array of topics in the game engine's global dict
        self.setGlobalDictValue("topics", selectedTopics)

        # Create a stats entry for each of the topics in the game engine's global dict
        questionStats = []
        for topic in selectedTopics:
            stats = {"topic": topic, "correct": 0, "incorrect": 0}
            questionStats.append(stats)
        self.setGlobalDictValue("questionStats", questionStats)

        # Start the game runtime timer
        self.startGameTimerInterval()
        
        # Show the main game interface
        self.showMainGameInterface()
    #------------------------------#

    #------------------------------#
    # Function that shows the main game interface 
    def showMainGameInterface(self, newGame=True):
        self.mainInterface = MainInterface(parentID=self.gameObjectID, newGame=newGame)

        mainInterfaceID = self.mainInterface.getGameObjectID()
        self.setSignalListener(msg="return-to-main-menu", sourceID=mainInterfaceID, callback=self.returnToMainMenu)
        self.setSignalListener(msg="quit-game", sourceID=mainInterfaceID, callback=self.quitGame)
    #------------------------------#

    #------------------------------#
    # Function that shows the Scoreboard interface  
    def showScoreboard(self):
        self.scoreboard = Scoreboard(parentID=self.gameObjectID)
        self.setSignalListener(msg="close-scoreboard", sourceID=self.scoreboard.getGameObjectID(), callback=self.closeScoreboard)
    #------------------------------#

    #------------------------------#
    # Function that closes the Scoreboard interface and shows the Main Menu again
    def closeScoreboard(self, _):
        self.removeSignalListenerBySourceID(self.scoreboard.getGameObjectID())
        self.scoreboard.__del__()
        self.showMainMenu()
    #------------------------------#

    #------------------------------#
    # Function that closes the Load Game Interface and shows the Main Menu again   
    def closeLoadGameInterface(self, _):
        self.removeSignalListenerBySourceID(self.loadGameInterface.getGameObjectID())
        self.loadGameInterface.__del__()
        self.showMainMenu()
    #------------------------------#

    #------------------------------#
    # Function that closes the Character Creator and shows the Main Menu again    
    def closeCharacterCreator(self, _):
        self.removeSignalListenerBySourceID(self.characterCreatorInterface.getGameObjectID())
        self.characterCreatorInterface.__del__()
        self.showMainMenu()
    #------------------------------#
        
    #------------------------------#
    # Function that returns to the Main Menu from the Main Interface after stopping the preexisting Timer thread
    def returnToMainMenu(self, _):
        self.mainInterface.__del__()
        if GameEngine.timer != None:
            GameEngine.timer.__del__()
            GameEngine.timer = None
        GameEngine.characterLoaded = False
        self.showMainMenu()
    #------------------------------#

    #------------------------------#
    # Function that quits the game after the Main Interface asks to do so
    def quitGame(self, _):
        self.mainInterface.__del__()
        GameEngine.quitGame()
    #------------------------------#
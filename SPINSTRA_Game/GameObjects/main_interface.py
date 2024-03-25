from .game_object import GameObject
from constants import *
from .map_overview import MapOverview
from .battle_interface import BattleInterface
from .treasure_interface import TreasureInterface
from .game_over_screen import GameOverScreen
from .game_finished_screen import GameFinishedScreen
from utils import *
import random

# Class that implements the Main Interface of the game
class MainInterface(GameObject):
    #------------------------------#
    # Constructor Function
    def __init__(self, parentID="", newGame=False):
        super().__init__()
        self.character = self.getGlobalDictValue("character")
        self.parentID = parentID
        self.initializeMapOverview(newGame)
    #------------------------------#

    #------------------------------#
    # Function that initializes the Map Overview
    def initializeMapOverview(self, newGame):
        self.mapOverview = MapOverview(self.gameObjectID, newGame)
        mapOverviewID = self.mapOverview.getGameObjectID()
        self.setSignalListener(msg="room-entered", sourceID=mapOverviewID, callback=self.roomEntered)
        self.setSignalListener(msg="game-finished", sourceID=mapOverviewID, callback=self.gameFinished)
    #------------------------------#

    #------------------------------#
    # Function that is called when a user enters a room
    def roomEntered(self, roomData):
        # Determine the difficulty of the room
        roomDifficulty = self.determineRoomDifficulty(roomData["type"] == "Boss")

        # If the room is a mystery room, do a weighted dice roll to determine what the room will actually be
        if roomData["type"] == "Mystery":
            possibleTypes = ["Battle", "Treasure"]
            roomType = random.choices(possibleTypes, weights=[.75, .25])[0]
            roomData["type"] = roomType

        # Show the appropriate interface based on the type of room
        if roomData["type"] == "Battle":
            self.showBattleInterface(roomDifficulty)
        if roomData["type"] == "Treasure":
            self.showTreasureInterface(roomDifficulty, False)
        if roomData["type"] == "Key":
            self.showTreasureInterface(roomDifficulty, True)
        if roomData["type"] == "Boss":
            self.showBattleInterface(roomDifficulty, isBossFight=True)
    #------------------------------#

    #------------------------------#
    # Function that sets the difficulty of the room the user is about to enter     
    def determineRoomDifficulty(self, isBossRoom):
        # Get the max difficulty value for the current level
        levelMaxDifficulty = self.getGlobalDictValue("currentLevelData")["maxDifficulty"]

        # If it's a boss room, it is automatically max difficulty. Otherwise, do a dice roll to determine what it will be
        if (isBossRoom):
            roomDifficulty = levelMaxDifficulty
        else:
            roomDifficulty = random.randint(0, levelMaxDifficulty)
        return roomDifficulty
    #------------------------------#


    #------------------------------#
    # Function that hides the Map Overview and shows the Battle Interface
    def showBattleInterface(self, roomDifficulty, isBossFight=False):
        # Hide the map overview
        self.mapOverview.hide()

        # Let the game engine know that we opened the Battle Interface
        self.setBattleInterfaceOpenStatus(True)

        # Show the battle interface - randomly choose an enemy type (or a boss type if appropriate) for the user to fight
        if (not isBossFight):
            enemyTypes = self.getGlobalDictValue("enemies")
            selectedEnemy = random.choice(enemyTypes)
        else:
            bossTypes = self.getGlobalDictValue("bosses")
            selectedEnemy = random.choice(bossTypes)

        # Set the selected enemy in the game engine's global dictionary
        self.setGlobalDictValue("enemy", selectedEnemy)
        self.battleInterface = BattleInterface(roomDifficulty=roomDifficulty, isBossFight=isBossFight, parentID=self.gameObjectID)

        # Set event listeners to detect when the battle ends
        battleInterfaceID = self.battleInterface.getGameObjectID()
        self.setSignalListener(msg="battle-over", sourceID=battleInterfaceID, callback=self.hideBattleInterface)
        self.setSignalListener(msg="flee-battle", sourceID=battleInterfaceID, callback=self.hideBattleInterface)
        if (isBossFight):
            self.setSignalListener(msg="boss-defeated", sourceID=battleInterfaceID, callback=self.progressToNextLevel)
    #------------------------------#

    #------------------------------#
    # Function that marks the current room as "completed"
    def markCurrentRoomComplete(self):
        currentLevelData = self.getGlobalDictValue("currentLevelData")
        roomData = currentLevelData["roomData"]
        currentLocation = currentLevelData["currentLocation"]

        for room in roomData:
            if room["coordinates"][0] == currentLocation[0] and room["coordinates"][1] == currentLocation[1]:
                room["completed"] = True
                break
    #------------------------------#

    #------------------------------#
    # Function that hides the Battle Interface and shows the Map Overview
    def hideBattleInterface(self, roomExitCondition):
        # Delete the Battle Interface game object and remove any signal listeners
        battleInterfaceID = self.battleInterface.getGameObjectID()
        self.battleInterface.__del__()
        self.removeSignalListenerBySourceID(battleInterfaceID)
        self.deleteGlobalDictValue("enemy")

        # Let the game engine know we closed the Battle Interface
        self.setBattleInterfaceOpenStatus(False)

        if roomExitCondition == "failure":
            self.showGameOverScreen
        else:
            # If the user successfully completed the room (as opposed to just fleeing the battle), mark it complete
            if roomExitCondition == "success":
                self.markCurrentRoomComplete()
            
            # Save the game 
            self.saveGame()

            # Show the map overview again
            self.mapOverview.show()
    #------------------------------#

    #------------------------------#
    # Function that hides the Map Overview and shows the Treasure Interface
    def showTreasureInterface(self, roomDifficulty, isBossKeyRoom):
        # Hide the map overview
        self.mapOverview.hide()

        # Initialize the Treasure Interface and set a signal listener
        self.treasureInterface = TreasureInterface(roomDifficulty=roomDifficulty, isBossKeyRoom=isBossKeyRoom, parentID=self.gameObjectID)
        self.setSignalListener("room-finished", sourceID=self.treasureInterface.getGameObjectID(), callback=self.hideTreasureInterface)
    #------------------------------#

    #------------------------------#
    # Function that hides the Treasure Interface and shows the Map Overview
    def hideTreasureInterface(self, result):
        # Delete the treasure interface
        self.removeSignalListenerBySourceID(self.treasureInterface.getGameObjectID())
        self.treasureInterface.__del__()

        # If the user successfully completed the room, mark it complete
        if result:
            self.markCurrentRoomComplete()

        # Save the game
        self.saveGame()

        # Show the map overview again
        self.mapOverview.show()
    #------------------------------#

    #------------------------------#
    # Function that shows the Game Over screen
    def showGameOverScreen(self):
        # Let the game engine know that we've opened the Game Over Screen
        self.setGameOverScreenOpenStatus(True)

        # Initialize the Game Over Screen and set signal listeners
        self.gameOverScreen = GameOverScreen(parentID=self.gameObjectID)
        gameOverScreenID = self.gameOverScreen.getGameObjectID()
        self.setSignalListener(msg="return-to-main-menu", sourceID=gameOverScreenID, callback=self.returnToMainMenu)
        self.setSignalListener(msg="quit-game", sourceID=gameOverScreenID, callback=self.quitGame)
    #------------------------------#

    #------------------------------#
    # Function that is called when a character defeats a boss and needs to progress to the next level   
    def progressToNextLevel(self, _):
        # Delete the Battle Interface
        self.removeSignalListenerBySourceID(self.battleInterface.getGameObjectID())
        self.battleInterface.__del__()

        # Let the game engine know we closed the Battle Interface
        self.setBattleInterfaceOpenStatus(False)

        # Delete the "enemy" value from the game engine's global dict
        self.deleteGlobalDictValue("enemy")

        # Mark the current room as complete
        self.markCurrentRoomComplete()
        
        # Tell the map overview to go to the next level
        self.mapOverview.goToNextLevel()

        # Save the game
        self.saveGame()
    #------------------------------#

    #------------------------------#
    # Function that is called when a user successfully completes the game       
    def gameFinished(self, _):
        # Ask the game engine to register the user's score on the locally-stored scoreboard
        self.registerScoreOnScoreboard()

        # Initialize the Game Finished Screen
        gameFinishedScreen = GameFinishedScreen(parentID=self.gameObjectID)
    #------------------------------#
        
    #------------------------------#
    # Function that emits the "Return to Main Menu" signal
    def returnToMainMenu(self, _):
        self.gameOverScreen.__del__()
        self.setGameOverScreenOpenStatus(False)
        self.emitSignal(msg="return-to-main-menu", data=None, targetID=self.parentID)
    #------------------------------#

    #------------------------------#
    # Function that emits the "Quit Game" signal
    def quitGame(self, _):
        self.gameOverScreen.__del__()
        self.emitSignal(msg="quit-game", data=None, targetID=self.parentID)
    #------------------------------#
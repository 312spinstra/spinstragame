from engine_initialization import GameEngine
from utils import formatNumberString

# Class that implements a Game Object
class GameObject:
    #------------------------------#
    # Constructor Function
    def __init__(self, zIndex=0):
        self.zIndex = zIndex
        gameObjectInfo = GameEngine.addGameObject(self)
        self.gameObjectID = gameObjectInfo["id"]
        self.gameObjectIndex = gameObjectInfo["index"]
        self.eventSubID = None
        self.eventSubIndex = None
        self.quit = False
        self.signalListeners = []
        self.focus()
    #------------------------------#

    #------------------------------#
    # Destructor Function
    def __del__(self):
        # Ask the game engine to remove you from its list of game objects
        GameEngine.removeGameObject(self.gameObjectID)
    #------------------------------#

    #------------------------------#
    # Function that subscribes the Game Object to the Engine's event pipeline
    def focus(self):
        eventSubInfo = GameEngine.subToEventPipeline(self)
        self.eventSubID = eventSubInfo["id"]
        self.eventSubIndex = eventSubInfo["index"]
    #------------------------------#

    #------------------------------#
    # Function that unsubscribes the Game Object from the Engine's event pipeline
    def unfocus(self):
        GameEngine.unsubFromEventPipeline(self.eventSubIndex)
    #------------------------------#

    #------------------------------#
    # Function that returns the Game Object ID
    def getGameObjectID(self):
        return self.gameObjectID
    #------------------------------#

    #------------------------------#
    # Function that emits a signal to a target Game Object
    def emitSignal(self, msg, data, targetID):
        signal = {"msg": msg, "sourceID": self.gameObjectID, "data": data}
        GameEngine.sendSignal(signal, targetID)
    #------------------------------#

    #------------------------------#
    # Function that sets a listener for a specified signal from a specific source
    def setSignalListener(self, msg, sourceID="", callback=lambda: True):
        listener = {"msg": msg, "sourceID": sourceID, "callback": callback}
        self.signalListeners.append(listener)
    #------------------------------#

    #------------------------------#
    # Function that removes a specified signal listener by sourceID
    def removeSignalListenerBySourceID(self, sourceID):
        for listener in self.signalListeners:
            if listener["sourceID"] == sourceID:
                self.signalListeners.remove(listener)
    #------------------------------#

    #------------------------------#
    # Function that removes a specified signal listener by message
    def removeSignalListenerByMsg(self, msg):
        for listener in self.signalListeners:
            if listener["msg"] == msg:
                self.signalListeners.remove(listener)
    #------------------------------#

    #------------------------------#
    # Function that handles any incoming signals and fires the appropriate callback
    def handleSignal(self, signal):
        for listener in self.signalListeners:
            if listener["msg"] == signal["msg"] and listener["sourceID"] == signal["sourceID"]:
                listener["callback"](signal["data"])
                break
    #------------------------------#

    #------------------------------#
    # Function that returns the Game Object's zIndex
    def getZIndex(self):
        return self.zIndex
    #------------------------------#

    #------------------------------#
    # Function that updates the Game Object (just a placeholder - can be overwritten in child class)
    def update(self, frameCounter, deltaTime):
        return
    #------------------------------#

    #------------------------------#
    # Function that renders the Game Object (just a placeholder - can be overwritten in child class)
    def render(self, canvas):
        return
    #------------------------------#

    #------------------------------#
    # Function that handles user interaction (just a placeholder - can be overwritten in child class)
    def handleInteraction(self, event, action, mousePos):
        return
    #------------------------------#

    #------------------------------#
    # Function that gets a value from the Game Engine's global dictionary
    def getGlobalDictValue(self, key):
        value = None
        if key in GameEngine.globalDict.keys():
            value = GameEngine.globalDict[key]
        return value
    #------------------------------#

    #------------------------------#
    # Function that sets a value in the Game Engine's global dictionary
    def setGlobalDictValue(self, key, value):
        if key in GameEngine.globalDict.keys():
            GameEngine.updateGlobalDictValue(key, value)
        else:
            GameEngine.addGlobalDictValue(key, value)
    #------------------------------#

    #------------------------------#
    # Function that deletes a value from the Game Engine's global dictionary
    def deleteGlobalDictValue(self, key):
        GameEngine.deleteGlobalDictValue(key)
    #------------------------------#

    #------------------------------#
    # Function that calls the Game Engine to save the user's progress
    def saveGame(self):
        GameEngine.saveGame()
    #------------------------------#

    #------------------------------#
    # Function that calls the Game Engine to attempt to load a previously-saved game
    def loadGame(self, password):
        return GameEngine.loadGame(password)
    #------------------------------#

    #------------------------------#
    # Function that calls the Game Engine to attempt to create a new character
    def attemptCreateCharacter(self, characterName, characterPassword):
        return GameEngine.attemptCreateCharacter(characterName, characterPassword)
    #------------------------------#

    #------------------------------#
    # Function that calls the Game Engine to get a question on a specific topic
    def getQuestion(self, difficulty):
        return GameEngine.getQuestion(difficulty)
    #------------------------------#

    #------------------------------#
    # Function that calls the Game Engine to register success/failure on a particular question in the stats
    def registerQuestionResult(self, result):
        GameEngine.registerQuestionResult(result)
    #------------------------------#

    #------------------------------#
    # Function that starts the interval to update the Game Engine's game runtime timer
    def startGameTimerInterval(self, initialValue=0):
        GameEngine.startGameTimerInterval(initialValue)
    #------------------------------#

    #------------------------------#
    # Function that pauses the updating of the Game Engine's game runtime timer
    def pauseGameTimer(self):
        GameEngine.pauseGameTimer()
    #------------------------------#

    #------------------------------#
    # Function that resumes the updating of the Game Engine's game runtime timer
    def resumeGameTimer(self):
        GameEngine.resumeGameTimer()
    #------------------------------#
    
    #------------------------------#
    # Function that returns a stringified version of the Game Engine's game runtime timer value in "hh:mm:ss" format   
    def getGameRuntime(self):
        return GameEngine.getGameRuntime()
    #------------------------------#

    #------------------------------#
    # Function that returns the user's current score
    def getUserScore(self):
        return self.getGlobalDictValue("userScore")
    #------------------------------#

    #------------------------------#
    # Function that increase's the user's score by a specified amount
    def increaseUserScore(self, amount):
        score = self.getUserScore()
        score += amount
        self.setGlobalDictValue("userScore", score)
    #------------------------------#

    #------------------------------#
    # Function that register's the user's stats on the locally-stored scoreboard   
    def registerScoreOnScoreboard(self):
        GameEngine.registerScoreOnScoreboard()
    #------------------------------#
        
    #------------------------------#
    # Function that sets the state of the "battleInterfaceOpen" property in the Game Engine 
    def setBattleInterfaceOpenStatus(self, status):
        GameEngine.setBattleInterfaceOpenStatus(status)
    #------------------------------#

    #------------------------------#
    # Function that sets the state of the "gameOverScreenOpen" property in the Game Engine   
    def setGameOverScreenOpenStatus(self, status):
        GameEngine.setGameOverScreenOpenStatus(status)
    #------------------------------#
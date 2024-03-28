import sys
import math
import threading
import random
import pygame
import GameObjects
import ast
from utils import *
from constants import *
from GameOperation import Repeat

""" CEngine is a custom Game Engine that was built from scratch expressly for this game.
    That being said, feel free to investigate the engine's code and improve it! It's definitely
    not perfect.
    
    The engine depends on pygame to create and maintain the game window and to render game objects to the screen.
    It also utilizes pygame's event system to detect and analyze user interaction. It relays this event information
    to the game objects and lets them determine how to respond. However, the engine does directly respond to the user
    pressing the 'esc' key. This was done because the engine has to pause the rendering of all active Game Objects in
    order to show the pause menu and must resume their rendering when the user exits the pause menu.

    As mentioned above, the engine will, unless the pause menu is open, render any active Game Objects that it knows of.
    In order to make a Game Object stop rendering, it must be deleted from the engine. Therefore, one must be cognizant
    to always clean up child Game Objects by calling their built-in destructor method, which takes care of removing them
    from the engine's render pipeline.

    The engine renders game objects in an order corresponding to their 'zIndex' value. In other words, game objects with a lower 'zIndex'
    are rendered before those with higher 'zIndex' values. This enables layering of game objects on top of one another.
    That's about as fancy as the rendering gets with this engine. In other words, it's only capable of 2D. Feel free
    to write support for three-dimensional rendering if you feel up to it!

    The game engine's memory is implemented in the form of a dictionary called 'globalDict'. In the early stages of development, I
    realized that the Game Objects needed access to a shared memory space in order to easily share data with one another. In other languages,
    this could have been done quite simply with a reference to globally-defined block of memory. However, in Python, we are not given
    direct access to reference. The only built-in Python data structure which allows access to values by reference is the dictionary, so
    this is what I went with. In other words, the expression "gRuntime = globalDict['gameRuntime']" actually assigns the reference to the 'gameRuntime'
    value into the 'gRuntime' variable. Other Python data structures would simply copy the value associated with the 'gameRuntime' key 
    into the 'gRuntime' variable.

    Additionally, the engine implements a communication system between game objects. Game Objects can emit 'signals' to
    other Game Objects with a data payload. However, the target Game Object will not receive that 'signal' unless it was
    listening for it in the first place. This system is what makes communication between parent and child Game Objects possible.
    'Signals' were designed to replicate, in some way, the 'event' system of a web browser.
    
    Finally, the engine contains a few utility functions that can be called by Game Objects. These are fairly simple and self-explanatory. """

# Function that implements CEngine
class CEngine:
    #------------------------------#
    # Constructor function
    def __init__(self, title="CEngine"):
        self.canvas = None
        self.clock = None
        self.gameObjects = []
        self.activeGameObjects = []
        self.frameCounter = 1
        self.fps = None
        self.deltaTime = None
        self.title = title
        self.globalDict = {}
        self.pauseMenuOpen = False
        self.pauseMenuID = None
        self.pauseMenuOptionIDs = []
        self.topicSelectionInterfaceOpen = False
        self.topicSelectionInterfaceID = None
        self.topicSelectionElementIDs = []
        self.statsInterfaceOpen = False
        self.statsInterfaceID = None
        self.statsInterfaceElementIDs = []
        self.characterLoaded = False
        self.battleInterfaceOpen = False
        self.gameOverScreenOpen = False
        self.currentTopic = None
        self.timer = None
        self.quit = False
    #------------------------------#

    #------------------------------#
    # Function that adds a game object to the game objects array
    def addGameObject(self, gameObject):
        # Create a game object ID
        id = self.createGameObjectID()

        # Initialize the game object dictionary, which is how the engine will see it
        newObj = {"id": id, "gameObject": gameObject, "zIndex": gameObject.zIndex}

        # Insert the game object into the game objects array in the appropriate rendering order
        newObjWasInserted = False
        for index, gameObj in enumerate(self.gameObjects):
            if gameObj["zIndex"] == newObj["zIndex"]:
                self.gameObjects.insert(index, newObj)
                newObjWasInserted = True
                break

        if not newObjWasInserted:
            self.gameObjects.append(newObj)

        # Return the game object info
        return {"id": id, "index": len(self.gameObjects) - 1}
    #------------------------------#

    #------------------------------#
    # Function that adds a key-value pair to the global dictionary
    def addGlobalDictValue(self, key, value):
        self.globalDict[key] = value
    #------------------------------#

    #------------------------------#
    # Function that creates a game object ID
    def createGameObjectID(self):
        utcTime = getUTCTime()
        utcParts = str(utcTime).split(".")
        convertedIDParts = [base36encode(int(utcParts[0])), base36encode(int(utcParts[1]))]
        convertedID = convertedIDParts[0] + "." + convertedIDParts[1]
        return convertedID
    #------------------------------#

    #------------------------------#
    # Function that creates an entry in the users file and creates a save file
    def createUserFiles(self, userID):
        # Create a save file with the name %userID%.save
        userSaveFile = open("Save_Files/" + userID + ".save", "x")
    #------------------------------#

    #------------------------------#
    # Function that creates a user ID
    def createUserID(self):
        utcTime = getUTCTime()
        utcParts = str(utcTime).split(".")
        convertedIDParts = [base36encode(int(utcParts[0])), base36encode(int(utcParts[1]))]
        convertedID = convertedIDParts[0] + "." + convertedIDParts[1]
        return convertedID
    #------------------------------#

    #------------------------------#
    # Function that removes a special key-value pair from the global dictionary
    def deleteGlobalDictValue(self, key):
        del(self.globalDict[key])
    #------------------------------#

    #------------------------------#
    # Function that increments the frame counter
    def incrementFrameCounter(self):
        if self.frameCounter == self.fps:
            self.frameCounter = 1
        else:
            self.frameCounter += 1
    #------------------------------#

    #------------------------------#
    # Function that initializes Pygame
    def initializePygame(self, screenWidth, screenHeight, fps=60):
        pygame.init()
        pygame.display.set_caption(self.title)
        pygame.mouse.set_cursor(*pygame.cursors.tri_left)
        self.canvas = pygame.display.set_mode((screenWidth, screenHeight))
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.deltaTime = math.ceil(1/self.fps * 1000)
    #------------------------------#

    #------------------------------#
    # Function that listens for interaction
    def listenForInteraction(self):
        action = "none"
        mousePos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            # Exit the application if the user wants to quit
            if event.type == pygame.QUIT:
                self.quitGame()

            # Report if the user left-clicked
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                action = "left-click"

            # Report if the user right-clicked
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                action = "right-click"

            # Report if the user used the mouse scroll wheel - this doesn't work for some reason
            if event.type == pygame.MOUSEWHEEL:
                action = "scroll"
            
            # Report if the user pressed a key
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    action = "up-arrow"
                if event.key == pygame.K_DOWN:
                    action = "down-arrow"
                if event.key == pygame.K_LEFT:
                    action = "left-arrow"
                if event.key == pygame.K_RIGHT:
                    action = "right-arrow"
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    action = "enter"
                if event.key == pygame.K_ESCAPE:
                    if self.pauseMenuOpen:
                        if ((not self.statsInterfaceOpen) and (not self.topicSelectionInterfaceOpen)):
                            self.closePauseMenu()
                    else:
                        self.openPauseMenu()
                    action = "escape"
                action = "normal keypress"

            # Report the interaction to all subscribed game objects
            #for obj in self.activeGameObjects:
            if not self.pauseMenuOpen:
                for obj in self.gameObjects:
                    obj["gameObject"].handleInteraction(event, action, mousePos)
            else:
                for obj in self.gameObjects:
                    if self.topicSelectionInterfaceOpen:
                        if obj["id"] in self.topicSelectionElementIDs:
                            obj["gameObject"].handleInteraction(event, action, mousePos)
                    elif self.statsInterfaceOpen:
                        if obj["id"] in self.statsInterfaceElementIDs:
                            obj["gameObject"].handleInteraction(event, action, mousePos)
                    else:
                        if obj["id"] in self.pauseMenuOptionIDs:
                            obj["gameObject"].handleInteraction(event, action, mousePos)
    #------------------------------#

    #------------------------------#
    # Function that removes a game object from the game objects array
    def removeGameObject(self, gameObjectID):
        for obj in self.gameObjects:
            if obj["id"] == gameObjectID:
                self.gameObjects.remove(obj)
                break
    #------------------------------#

    #------------------------------#
    # Function that renders the current game frame
    def render(self):
        self.canvas.fill((0,0,0))

        if not self.pauseMenuOpen:
            for obj in self.gameObjects:
                obj["gameObject"].render(self.canvas)
        else:
            for obj in self.gameObjects:
                if self.topicSelectionInterfaceOpen:
                    if obj["id"] in self.topicSelectionElementIDs:
                        obj["gameObject"].render(self.canvas)
                elif self.statsInterfaceOpen:
                    if obj["id"] in self.statsInterfaceElementIDs:
                        obj["gameObject"].render(self.canvas)
                else:
                    if obj["id"] in self.pauseMenuOptionIDs:
                        obj["gameObject"].render(self.canvas)

        pygame.display.flip()
    #------------------------------#

    #------------------------------#
    # Function that quits the game
    def quitGame(self):
        if self.timer != None:
            self.timer.__del__()
        self.quit = True
    #------------------------------#

    #------------------------------#
    # Function that runs the game
    def runGame(self):
        # Listen for interaction
        self.listenForInteraction()

        # Update game objects
        for obj in self.gameObjects:
            obj["gameObject"].update(self.frameCounter, self.deltaTime)

        # Update the frame counter
        self.incrementFrameCounter()

        # Render the current game frame
        self.render()

        # Tick the game clock
        self.deltaTime = self.clock.tick(self.fps)
    #------------------------------#

    #------------------------------#
    # Function that sends a signal, along with its data payload, to a specified Game Object
    def sendSignal(self, signal, targetID):
        # If the target is the Game Engine itself
        if targetID == "GameEngine":
            if (self.pauseMenuID != None and signal["sourceID"] == self.pauseMenuID):
                self.handlePauseMenuEvent(signal["data"])
            elif (self.topicSelectionInterfaceID != None and signal["sourceID"] == self.topicSelectionInterfaceID):
                self.closeTopicSelectionInterface(signal["data"])
            elif (self.statsInterfaceID != None and signal["sourceID"] == self.statsInterfaceID):
                self.closeStatsInterface(signal["data"])

        # If the target is a normal game object
        else:
            for obj in self.gameObjects:
                if obj["id"] == targetID:
                    obj["gameObject"].handleSignal(signal)
                    break
    #------------------------------#

    #------------------------------#
    # Function that subscribes an object to the event pipeline
    def subToEventPipeline(self, gameObject):
        id = getUTCTime()
        obj = {"id": id, "gameObject": gameObject}
        self.activeGameObjects.append(obj)
        return {"id": id, "index": len(self.activeGameObjects)-1}
    #------------------------------#

    #------------------------------#
    # Function that unsubscribes an element from the event pipeline
    def unsubFromEventPipeline(self, activeObjectIndex):
        del self.activeGameObjects[activeObjectIndex : activeObjectIndex+1]
    #------------------------------#

    #------------------------------#
    # Function that updates a value in the global dictionary
    def updateGlobalDictValue(self, key, newValue):
        self.globalDict[key] = newValue
    #------------------------------#

    #------------------------------#
    # Function that saves the game
    def saveGame(self):
        # Get the user's userID
        userID = self.globalDict["userID"]

        # Convert the global dictionary to a string
        global_dict_str = str(self.globalDict)

        # Encrypt the global dictionary
        encrypted_global_dict = RSA_Encrypt(global_dict_str, RSA_PUBLIC_KEY, RSA_PRIMES_PRODUCT)

        # Write it to a save file
        with open("Save_Files/" + userID + ".save", "w") as save_file:
            save_file.write(encrypted_global_dict)
            save_file.close()
    #------------------------------#

    #------------------------------#
    # Function that loads a game from a specified save file
    def loadGame(self, password):
        # Load the users file
        users = loadCSVFile("Engine/users.csv")

        # Search for a user with a matching password
        userID = None
        encodedPassword = RSA_Encrypt(password, RSA_PUBLIC_KEY, RSA_PRIMES_PRODUCT)

        for user in users:
            if user["password"] == encodedPassword:
                userID = user["userID"]
                break
        
        # If the user was not found, return False
        if userID == None:
            return False

        # Read the contents of a save file
        encrypted_contents = ""
        with open("Save_Files/" + userID + ".save", "r") as save_file:
            encrypted_contents = save_file.read()
            save_file.close()

        # Decrypt the contents
        decrypted_contents = RSA_Decrypt(encrypted_contents, RSA_PRIVATE_KEY, RSA_PRIMES_PRODUCT)

        # Set the global dictionary equal to the decrypted contents - after converting them from a string to a dictionary
        self.globalDict = ast.literal_eval(decrypted_contents)

        # Set the "characterLoaded" flag to True
        self.characterLoaded = True

        return True
    #------------------------------#

    #------------------------------#
    # Function that opens the Pause Menu
    def openPauseMenu(self):
        # Pause the game timer if it exists
        if (self.timer != None):
            self.pauseGameTimer()

        # Set the "pauseMenuOpen" flag
        self.pauseMenuOpen = True

        # Dynamically determine the pause menu options based on where the user is in the game
        pauseMenuOptions = []
        if not self.characterLoaded or self.battleInterfaceOpen or self.gameOverScreenOpen:
            pauseMenuOptions = ["Resume", "Quit"]
        else:
            pauseMenuOptions = PAUSE_MENU["options"]

        # Initialize and render the pause menu game object
        self.pauseMenu = GameObjects.Menu(PAUSE_MENU["title"], pauseMenuOptions, parentID="GameEngine", isPauseMenu=True)
        self.pauseMenuID = self.pauseMenu.getGameObjectID()
        self.pauseMenuOptionIDs = self.pauseMenu.getOptionGameObjectIDs()
    #------------------------------#

    #------------------------------#
    # Function that closes the Pause Menu
    def closePauseMenu(self):
        # Delete the pause menu game object
        self.pauseMenu.__del__()
        self.pauseMenu = None

        # Clean up any associated data
        self.pauseMenuOptionIDs = []
        self.pauseMenuOpen = False

        # Resume the game timer if it exists
        if (self.timer != None):
            self.resumeGameTimer()
    #------------------------------#

    #------------------------------#
    # Function that handles each user action possible from the Pause Menu
    def handlePauseMenuEvent(self, option):
        if option == "Resume":
            self.closePauseMenu()
        elif option == "View Stats":
            self.openStatsInterface()
        elif option == "Edit Review Topics":
            self.openTopicSelectionInterface()
        elif option == "Exit Without Saving" or option == "Quit":
            self.quitGame()
        elif option == "Save and Quit":
            self.saveGame()
            self.quitGame()
    #------------------------------#

    #------------------------------#
    # Function that attempts to create a character in the Engine's users file and returns the status
    def attemptCreateCharacter(self, characterName, characterPassword):
        # Encode the password so we aren't actually storing the real thing
        encodedPassword = RSA_Encrypt(characterPassword, RSA_PUBLIC_KEY, RSA_PRIMES_PRODUCT)

        # Load the contents of the users file
        users = loadCSVFile("Engine/users.csv")

        # Search the contents of the users file to see if there's already an entry with a matching name and encoded password
        for user in users:
            if user["name"] == characterName and user["password"] == encodedPassword:
                return False

        # Otherwise, continue. Create a userID and make the user files
        userID = self.createUserID()
        self.globalDict["userID"] = userID
        self.createUserFiles(userID)

        # Create a new record in the users file with the name, encoded password, and newly-created user ID
        newUserRecord = {"name": characterName, "password": encodedPassword, "userID": userID}
        users.append(newUserRecord)

        # Write the new record to the users file
        writeCSVFile("Engine/users.csv", ["name", "password", "userID"], users)

        # Set the "characterLoaded" flag
        self.characterLoaded = True

        return True
    #------------------------------#

    #------------------------------#
    # Function that gets a question of a particular topic
    def getQuestion(self, difficulty):
        # Randomly choose a topic from the list of Review Topics that the user has configured
        topic = random.choice(self.globalDict["topics"])

        # Set the current topic
        self.currentTopic = topic

        # Construct the filepath to the appropriate CSV file
        filepath = "Data/Questions/" + topic.lower() + "/questions.csv"

        # Load the questions from the CSV file
        unfilteredQuestions = loadCSVFilequestions(filepath)

        # Get all questions less than or equal to the requested difficulty max
        questions = []
        for x in filter(lambda x: int(x['Difficulty']) <= difficulty, unfilteredQuestions):
            questions.append(x)

        # Get the array of seen question IDs
        seenQuestionIDs = self.globalDict['seenQuestionIDs']

        # Select an unseen question if at all possible
        questionSelected = False
        selectedQuestion = None
        numIterations = 0

        while (not questionSelected):
            # Select a random question index
            randomIndex = random.randrange(len(questions))
            selectedQuestion = questions[randomIndex]

            # Hash the question to get the question ID
            questionID = hash(selectedQuestion['Question'])

            # Check if an exit condition has been reached
            if (not(questionID in seenQuestionIDs) or (numIterations >= len(questions))):
                questionSelected = True
                self.currentQuestion = selectedQuestion

            # Increment the iteration counter
            numIterations += 1

        # Determine the question type
        selectedQuestion = determineQuestionType(selectedQuestion)

        # Set the question score based on the difficulty
        score = 10 + (10 * difficulty)
        selectedQuestion["score"] = score
        
        # Return the selected question
        return selectedQuestion
    #------------------------------#

    #------------------------------#
    # Function that opens the Topic Selection Interface
    def openTopicSelectionInterface(self):
        self.topicSelectionInterfaceOpen = True
        selectedTopics = self.globalDict["topics"].copy()
        self.topicSelectionInterface = GameObjects.TopicSelectionInterface(parentID="GameEngine", selectedTopics=selectedTopics)
        self.topicSelectionInterfaceID = self.topicSelectionInterface.getGameObjectID()
        self.topicSelectionElementIDs = self.topicSelectionInterface.getElementIDs()
    #------------------------------#

    #------------------------------#
    # Function that closes the Topic Selection Interface   
    def closeTopicSelectionInterface(self, selectedTopics):
        # Get a list of any new topics the user selected
        newTopics = []
        for topic in selectedTopics:
            if not (topic in self.globalDict["topics"]):
                newTopics.append(topic)

        # Add new question stats for all new review topics
        for topic in newTopics:
            newTopicStats = {"topic": topic, "correct": 0, "incorrect": 0}
            self.globalDict["questionStats"].append(newTopicStats)

        # Update the topics array and close the Topic Selection Interface
        self.updateGlobalDictValue("topics", selectedTopics)
        self.topicSelectionInterface.__del__()
        self.topicSelectionElementIDs = []
        self.topicSelectionInterfaceID = None
        self.topicSelectionInterfaceOpen = False
    #------------------------------#

    #------------------------------#
    # Function that opens the Question Stats Interface   
    def openStatsInterface(self):
        self.statsInterfaceOpen = True
        self.statsInterface = GameObjects.QuestionStatsInterface(parentID="GameEngine")
        self.statsInterfaceID = self.statsInterface.getGameObjectID()
        self.statsInterfaceElementIDs = self.statsInterface.getElementIDs()
    #------------------------------#

    #------------------------------#
    # Function that closes the Question Stats Interface  
    def closeStatsInterface(self, _):
        self.statsInterface.__del__()
        self.statsInterfaceElementIDs = []
        self.statsInterfaceID = None
        self.statsInterfaceOpen = False
    #------------------------------#

    #------------------------------#
    # Function that registers the user's success/failure with a question in the stats
    def registerQuestionResult(self, result):
        # Increment the correct/incorrect counters as necessary in the appropriate topic stats entry
        for stats in self.globalDict["questionStats"]:
            if stats["topic"] == self.currentTopic:
                if result:
                    stats["correct"] += 1
                else:
                    stats["incorrect"] += 1
                break

        # If the user successfully answered the question, add the question ID to the array of seen IDs so that they won't see it for a while
        if result:
            questionID = hash(self.currentQuestion['Question'])
            if (not (questionID in self.globalDict['seenQuestionIDs'])):
                self.globalDict['seenQuestionIDs'].append(questionID)

        # Reset the current topic and current question
        self.currentTopic = None
        self.currentQuestion = None
    #------------------------------#

    #------------------------------#
    # Function that starts the game timer interval
    def startGameTimerInterval(self, initialValue=0):
        self.timer = GameObjects.Timer(initialValue)
        self.timer.startTimer()
    #------------------------------#

    #------------------------------#
    # Function that pauses the game timer      
    def pauseGameTimer(self):
        self.timer.pauseTimer()
    #------------------------------#

    #------------------------------#
    # Function that resumes the game timer
    def resumeGameTimer(self):
        self.timer.resumeTimer()
    #------------------------------#
        
    #------------------------------#
    # Function that returns a stringified version of the Game Engine's game runtime timer value in "hh:mm:ss" format
    def getGameRuntime(self):
        gameRuntimeSeconds = int(str(self.globalDict["gameRuntime"]))

        hoursString = "00"
        minutesString = "00"
        secondsString = "00"

        if (gameRuntimeSeconds >= 3600):
            hours = gameRuntimeSeconds//3600
            remainingSeconds = gameRuntimeSeconds - (hours * 3600)

            minutes = remainingSeconds//60
            minutesString = formatNumberString(minutes)

            remainingSeconds = gameRuntimeSeconds - (minutes * 60)
            secondsString = formatNumberString(remainingSeconds)

            gameRuntimeSeconds = 0
        elif (gameRuntimeSeconds >= 60):
            minutes = gameRuntimeSeconds//60
            minutesString = formatNumberString(minutes)

            remainingSeconds = gameRuntimeSeconds - (minutes * 60)
            secondsString = formatNumberString(remainingSeconds)

            gameRuntimeSeconds = 0
        else:
            secondsString = formatNumberString(gameRuntimeSeconds)

        return hoursString + ":" + minutesString + ":" + secondsString
    #------------------------------#

    #------------------------------#
    # Function that adds an entry to the locally-stored scoreboard   
    def registerScoreOnScoreboard(self):
        # Pause the game timer if it exists
        if (self.timer != None):
            self.pauseGameTimer()
        
        # Load the scores CSV file
        scores = loadCSVFile(SCOREBOARD_FILEPATH)

        # Create a new entry for the current user
        entry = {"Name": self.globalDict["character"]["name"], "Score": self.globalDict["userScore"], "Time": self.getGameRuntime()}

        # Append the entry to the list of scores
        scores.append(entry)

        # Write the scores list to the CSV file
        writeCSVFile(SCOREBOARD_FILEPATH, ["Name", "Score", "Time"], scores)
    #------------------------------#

    #------------------------------#
    # Function that sets the state of the "battleInterfaceOpen" property   
    def setBattleInterfaceOpenStatus(self, status):
        self.battleInterfaceOpen = status
    #------------------------------#

    #------------------------------#
    # Function that sets the state of the "gameOverScreenOpen" property    
    def setGameOverScreenOpenStatus(self, status):
        self.gameOverScreenOpen = status
    #------------------------------#
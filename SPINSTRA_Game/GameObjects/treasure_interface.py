from .game_object import GameObject
from .question_modal import QuestionModal
from .multiple_choice_question_modal import MultipleChoiceQuestionModal
from .feedback_window import FeedbackWindow
from .battle_info_window import BattleInfoWindow
from .icon import Icon
from constants import *
import random

# Class that implements the Treasure Interface
class TreasureInterface(GameObject):
    #------------------------------#
    # Constructor Function
    def __init__(self, roomDifficulty=0, isBossKeyRoom=False, parentID="", zIndex=0):
        super().__init__(zIndex=zIndex)
        self.parentID = parentID
        self.currentQuestionFeedback = None
        self.currentQuestionScore = None
        self.questionModal = None
        self.feedbackWindow = None
        self.infoWindow = None
        self.treasureChestIcon = None

        self.roomDifficulty = roomDifficulty
        self.isBossKeyRoom = isBossKeyRoom
        
        if self.isBossKeyRoom:
            self.item = {"name": "Boss Key", "assetPath": "Assets/Items/Boss_Key/Boss_Key.png", "description": "The key that opens the Boss Room at the end of the level. This item is automatically used upon entering the Boss Room."}
        else:
            self.item = None

        self.interfaceElements = []

        if not self.isBossKeyRoom:
            self.getItemChoice()

        self.initializeElements()
    #------------------------------#

    #------------------------------#
    # Destructor Function
    def __del__(self):
        for el in self.interfaceElements:
            el.__del__()

        if (self.questionModal != None):
            self.questionModal.__del__()

        if (self.feedbackWindow != None):
            self.feedbackWindow.__del__()

        if (self.infoWindow != None):
            self.infoWindow.__del__()

        if (self.treasureChestIcon != None):
            self.treasureChestIcon.__del__()

        super().__del__()
    #------------------------------#

    #------------------------------#
    # Function that randomly chooses and item from the global items array
    def getItemChoice(self):
        # Compile a list of the pre-defined item rarities
        itemTypes = self.getGlobalDictValue("items")
        probabilities = []
        for itemType in itemTypes:
            probabilities.append(float(itemType["rarity"]))

        # Make a weighted random choice to determine what the item will be
        self.item = random.choices(itemTypes, probabilities)[0]
    #------------------------------#

    #------------------------------#
    # Function that initializes the elements used in the user interface
    def initializeElements(self):
        # Intialize the treasure chest icon
        self.treasureChestIcon = Icon(TREASURE_CHEST_ICON_FILEPATH, SCREEN_WIDTH//2, SCREEN_HEIGHT-120, x=80, scale=12)

        # Parse the question info that was passed in
        questionInfo = self.getQuestion(self.roomDifficulty)
        question = questionInfo["Question"]
        answer = questionInfo["Answer"]
        questionType = questionInfo["type"]
        self.currentQuestionFeedback = questionInfo["Feedback"] if questionInfo["Feedback"] != None else "No feedback"
        self.currentQuestionScore = questionInfo["score"]

        # Spawn different types of question modals based on the questionType and set signal listeners
        if questionType == "multiple-choice":
            self.questionModal = MultipleChoiceQuestionModal(centerX=SCREEN_WIDTH//2, centerY=SCREEN_HEIGHT//2-100, width=800, height=600, question=question, answer=answer, questionInfo=questionInfo, incorrectAnswers=questionInfo["incorrectAnswers"], parentID=self.gameObjectID)
        else:
            self.questionModal = QuestionModal(centerX=SCREEN_WIDTH//2, centerY=SCREEN_HEIGHT//2-100, width=800, height=600, question=question, answer=answer, questionInfo=questionInfo, parentID=self.gameObjectID)

        questionModalID = self.questionModal.getGameObjectID()
        self.setSignalListener(msg="result-determined", sourceID=questionModalID, callback=self.resultDetermined)
        self.setSignalListener(msg="close-modal", sourceID=questionModalID, callback=self.modalClosed)
    #------------------------------#

    #------------------------------#
    # Function that is called when the user answers the question in the Question Modal
    def resultDetermined(self, result):
        # Register the result of the user answering the question with the game engine
        self.registerQuestionResult(result)

        # Delete the question modal
        self.questionModal.__del__()
        
        # If the user got the question right, add the item to their inventory
        if result:
            character = self.getGlobalDictValue("character")
            character["inventory"].append(self.item)
            self.increaseUserScore(self.currentQuestionScore)
            infoMessage = "Received " + self.item["name"] + "!"
            self.infoWindow = BattleInfoWindow(info=infoMessage, secondsUntilClose=1, callbackArg=result, parentID=self.gameObjectID)
            infoWindowID = self.infoWindow.getGameObjectID()
            self.setSignalListener(msg="close", sourceID=infoWindowID, callback=self.completeRoom)
        else: # Otherwise, show the user feedback
            self.feedbackWindow = FeedbackWindow(title="Feedback:", feedback=self.currentQuestionFeedback, parentID=self.gameObjectID)
            feedbackWindowID = self.feedbackWindow.getGameObjectID()
            self.setSignalListener(msg="close", sourceID=feedbackWindowID, callback=self.feedbackWindowClosed)
    #------------------------------#

    #------------------------------#
    # Function that emits the room completion state  
    def completeRoom(self, result):
        roomCompletionState = True

        if (self.isBossKeyRoom):
            roomCompletionState = result

        self.emitRoomCompletionSignal(roomCompletionState)
    #------------------------------#

    #------------------------------#
    # Function that is called when the Question Modal is closed
    def modalClosed(self, _):
        if self.isBossKeyRoom:
            roomCompletionState = False
        else:
            roomCompletionState = True

        self.emitRoomCompletionSignal(roomCompletionState)
    #------------------------------#

    #------------------------------#
    # Function that is called when the room has been completed
    def emitRoomCompletionSignal(self, roomCompletionState):
        self.emitSignal(msg="room-finished", data=roomCompletionState, targetID=self.parentID)
    #------------------------------#
        
    #------------------------------#
    # Function that is called when the feedback window is closed   
    def feedbackWindowClosed(self, _):
        self.removeSignalListenerBySourceID(self.feedbackWindow.getGameObjectID())
        self.feedbackWindow.__del__()
        
        # If the user failed the question, and the reward was a boss key, don't mark the room complete.
        # The user needs the boss key to progress, so they need to be able to try again until they get it right.
        if self.isBossKeyRoom:
            roomCompletionState = False
        else:
            roomCompletionState = True

        self.completeRoom(roomCompletionState)
    #------------------------------#
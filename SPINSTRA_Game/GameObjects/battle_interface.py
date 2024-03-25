import pygame
import random
from .game_object import GameObject
from .interactive_rect import InteractiveRect
from .simple_text import SimpleText
from .animated_sprite import AnimatedSprite
from .healthbar import HealthBar
from .question_modal import QuestionModal
from .multiple_choice_question_modal import MultipleChoiceQuestionModal
from .feedback_window import FeedbackWindow
from .battle_info_window import BattleInfoWindow
from .items_window import ItemsWindow
from .special_abilities_window import SpecialAbilitiesWindow
from constants import *
from utils import *

# Class that implements the battle interface
class BattleInterface(GameObject):
    #------------------------------#
    # Constructor Function
    def __init__(self, roomDifficulty=0, isBossFight=False, parentID=""):
        super().__init__()
        self.roomDifficulty = roomDifficulty
        self.isBossFight = isBossFight
        self.parentID = parentID
        self.character = self.getGlobalDictValue("character")
        self.enemy = self.getGlobalDictValue("enemy")
        if self.isBossFight:
            self.enemy["HP"] = BOSS_ENEMY_BASE_HEALTH + (roomDifficulty * 10)
        else:
            self.enemy["HP"] = REGULAR_ENEMY_BASE_HEALTH + (roomDifficulty * 10)
        self.maxEnemyHealth = self.enemy["HP"]
        self.characterSprite = None
        self.enemySprite = None
        self.interfaceElements = []
        self.characterHealthBar = None
        self.enemyHealthBar = None
        self.turnIndicatorText = None
        self.currentQuestionInfo = None
        self.currentQuestionFeedback = None
        self.currentQuestionScore = None
        self.feedbackWindow = None
        self.optionsFont = pygame.font.Font(GAME_FONT_PATH, MED_FONT_SIZE)

        self.questionModal = None
        self.enemyQuestionModal = None
        self.battleInfoWindow = None

        self.turn = "character"

        self.disallowedAbilities = []

        self.righteousDefenseActive = False
        self.secondChanceActive = False
        self.sneakAttackActive = False

        self.stimulantActive = False
        self.stimulantTurnsleft = 0

        self.tonicActive = False

        self.autoReviveWasUsed = False

        self.defenseBuffActive = False

        self.initializeElements()
    #------------------------------#

    #------------------------------#
    # Destructor Function
    def __del__(self):
        for el in self.interfaceElements:
            el["rect"].__del__()

        self.characterSprite.__del__()
        self.enemySprite.__del__()

        if (self.questionModal != None):
            self.questionModal.__del__()

        if (self.enemyQuestionModal != None):
            self.enemyQuestionModal.__del__()

        self.turnIndicatorText.__del__()

        if (self.feedbackWindow != None):
            self.feedbackWindow.__del__()

        if (self.battleInfoWindow != None):
            self.battleInfoWindow.__del__()

        if (self.characterHealthBar != None):
            self.characterHealthBar.__del__()

        if (self.enemyHealthBar != None):
            self.enemyHealthBar.__del__()

        super().__del__()
    #------------------------------#

    #------------------------------#
    # Function that initializes all the elements for the battle interface
    def initializeElements(self):
        # Initialize character sprite and set a signal listener
        self.characterSprite = AnimatedSprite("Assets", self.character["type"]["animations"], centerX = 200, centerY = SCREEN_HEIGHT - 500, scaleFactor=3, parentID=self.gameObjectID, sendSignals=True, zIndex=5)
        characterSpriteID = self.characterSprite.getGameObjectID()
        self.setSignalListener(msg="animation-finished", sourceID=characterSpriteID, callback=self.endBattle)

        # Initialize enemy sprite and set a signal listener
        self.enemySprite = AnimatedSprite("Assets", self.enemy["animations"], centerX = SCREEN_WIDTH - 200, centerY = SCREEN_HEIGHT - 500, scaleFactor=3, mirror=True, parentID=self.gameObjectID, sendSignals=True, zIndex=5)
        enemySpriteID = self.enemySprite.getGameObjectID()
        self.setSignalListener(msg="animation-finished", sourceID=enemySpriteID, callback=self.endBattle)

        # Calculate the width and height of each of the battle options
        attackTextWidth, attackTextHeight = self.optionsFont.size("Attack")
        specialTextWidth, specialTextHeight = self.optionsFont.size("Special Abilities")
        itemsTextWidth, itemsTextHeight = self.optionsFont.size("Items")

        # Create the attack option and set a signal listener
        attackOptionRect = InteractiveRect(20, SCREEN_HEIGHT - 200 + 10, defaultColor=BATTLE_OPTIONS_BACKGROUND_COLOR, highlightColor=BATTLE_OPTIONS_BACKGROUND_COLOR, defaultTextColor=WHITE, highlightTextColor=BATTLE_TEXT_HIGHLIGHT_COLOR, text="Attack", textCoordinates=(20, SCREEN_HEIGHT - 200 + 10), width=attackTextWidth, height=attackTextHeight, fontSize=MED_FONT_SIZE, parentID=self.gameObjectID, callbackArg="attack", zIndex=1)
        self.interfaceElements.append({"name": "attackOption", "rect": attackOptionRect})

        self.setSignalListener(msg="clicked", sourceID=attackOptionRect.getGameObjectID(), callback=self.optionSelected)

        # Create the special abilities option and set a signal listener
        specialOptionRect = InteractiveRect(20, SCREEN_HEIGHT - 200 + 40, defaultColor=BATTLE_OPTIONS_BACKGROUND_COLOR, highlightColor=BATTLE_OPTIONS_BACKGROUND_COLOR, defaultTextColor=WHITE, highlightTextColor=BATTLE_TEXT_HIGHLIGHT_COLOR, text="Special Abilities", textCoordinates=(20, SCREEN_HEIGHT - 200 + 40), width=specialTextWidth, height=specialTextHeight, fontSize=MED_FONT_SIZE, parentID=self.gameObjectID, callbackArg="special", zIndex=1)
        self.interfaceElements.append({"name": "specialOption", "rect": specialOptionRect})

        self.setSignalListener(msg="clicked", sourceID=specialOptionRect.getGameObjectID(), callback=self.optionSelected)

        # Create the items option and set a signal listener
        itemsOptionRect = InteractiveRect(20, SCREEN_HEIGHT - 200 + 70, defaultColor=BATTLE_OPTIONS_BACKGROUND_COLOR, highlightColor=BATTLE_OPTIONS_BACKGROUND_COLOR, defaultTextColor=WHITE, highlightTextColor=BATTLE_TEXT_HIGHLIGHT_COLOR, text="Items", textCoordinates=(20, SCREEN_HEIGHT - 200 + 70), width=itemsTextWidth, height=itemsTextHeight, fontSize=MED_FONT_SIZE, parentID=self.gameObjectID, callbackArg="items", zIndex=1)
        self.interfaceElements.append({"name": "itemsOption", "rect": itemsOptionRect})

        self.setSignalListener(msg="clicked", sourceID=itemsOptionRect.getGameObjectID(), callback=self.optionSelected)

        # Set up the character and enemy health bar info
        healthBarText = "HP:"
        healthBarLabelWidth, healthBarLabelHeight = self.optionsFont.size(healthBarText)
        healthBarWidth = 300

        # Initialize the character and the enemy healthbars
        self.characterHealthBar = HealthBar(TLx=7, TLy=20, maxHealth=self.character["maxHealth"], initialHealth=self.character["HP"], parentID=self.gameObjectID)

        self.enemyHealthBar = HealthBar(TLx=SCREEN_WIDTH - healthBarWidth - healthBarLabelWidth - 12, TLy=20, maxHealth=self.maxEnemyHealth, initialHealth=self.enemy["HP"], parentID=self.gameObjectID)

        # Set up the turn indicator text
        indicatorText = "Character Turn"
        indicatorTextWidth, indicatorTextHeight = self.optionsFont.size(indicatorText)
        textX = SCREEN_WIDTH//2 - indicatorTextWidth//2
        textY = 10
        self.turnIndicatorText = SimpleText(text="Character Turn", fontSize=MED_FONT_SIZE, x=textX, y=textY)
    #------------------------------#

    #------------------------------#
    # Function that renders the command window background
    def render(self, canvas):
        # Set up the command window background rectangle
        commandContainerHeight = 200
        commandContainerWidth = SCREEN_WIDTH
        commandContainer = pygame.Rect(0, SCREEN_HEIGHT-commandContainerHeight, commandContainerWidth, commandContainerHeight)

        # Render the command window background and border rectangles
        pygame.draw.rect(canvas, BATTLE_OPTIONS_BACKGROUND_COLOR, commandContainer)
        pygame.draw.rect(canvas, WHITE, commandContainer, 2)
    #------------------------------#

    #------------------------------#
    # Function that handles when a button is pressed
    def optionSelected(self, option, defaultQuestionInfo=None):
        # If the user clicked "Attack"
        if option == "attack":
            # Use the default question info if it's set
            questionInfo = defaultQuestionInfo

            # Otherwise, get a random question from the game engine
            if defaultQuestionInfo == None:
                questionInfo = self.getQuestion(self.roomDifficulty)

            question = questionInfo["Question"]
            answer = questionInfo["Answer"]
            questionType = questionInfo["type"]
            self.currentQuestionInfo = questionInfo
            self.currentQuestionFeedback = questionInfo["Feedback"] if questionInfo["Feedback"] != None else "No feedback"
            self.currentQuestionScore = questionInfo["score"]

            # Spawn different types of question modals based on the questionType and set signal listeners
            if questionType == "multiple-choice":
                self.questionModal = MultipleChoiceQuestionModal(centerX=SCREEN_WIDTH//2, centerY=SCREEN_HEIGHT//2-100, width=800, height=600, question=question, answer=answer, questionInfo=questionInfo, incorrectAnswers=questionInfo["incorrectAnswers"].copy(), parentID=self.gameObjectID)
            else:
                self.questionModal = QuestionModal(centerX=SCREEN_WIDTH//2, centerY=SCREEN_HEIGHT//2-100, width=800, height=600, question=question, answer=answer, questionInfo=questionInfo, parentID=self.gameObjectID)

            questionModalID = self.questionModal.getGameObjectID()
            self.setSignalListener(msg="result-determined", sourceID=questionModalID, callback=self.resultDetermined)
            self.setSignalListener(msg="close-modal", sourceID=questionModalID, callback=self.closeQuestionModal)

            # Disable the options in the command window so that the user has to interact with the question modal
            self.disableButtons()

        # If the user clicked "Items"
        if option == "items":
            # Show the items window
            self.showItemsWindow()

        # If the user clicked "Special Abilities"
        if option == "special":
            # Show the special abilities window
            self.showSpecialAbilitiesWindow()
    #------------------------------#

    #------------------------------#
    # Function that runs the logic for performing an attack
    def performAttack(self, attacker):
        # If the character is attacking the enemy
        if attacker == "character":
            # Use the base hit value unless the character has used a "Stimulant" item
            hitValue = 10
            if self.stimulantActive:
                hitValue += 10
                self.stimulantTurnsleft -= 1
                if (self.stimulantTurnsleft == 0):
                    self.stimulantActive = False

            # Decrement the enemy's health and update their health bar
            self.enemy["HP"] -= hitValue
            self.enemyHealthBar.updateHealthValue(self.enemy["HP"])

            # Perform the character's attack animation
            self.characterSprite.selectAnimation("Attack", True, True)

            # Perform either the enemy's "Hit" or the "Death" animation based on their remaining heath value
            if (self.enemy["HP"] <= 0):
                self.enemySprite.selectAnimation("Death", True, False)
            else:
                self.enemySprite.selectAnimation("Hit", True, True)

        # If the enemy is attacking the character
        if attacker == "enemy":
            # Hit the character unless they've used the "Righteous Defense" special ability
            if not self.righteousDefenseActive:
                # Use the base hit value unless it's a boss enemy, then do double damage
                hitValue = 10
                if self.isBossFight:
                    hitValue = 20

                # If the character has used a "Tonic" item, reduce the amount of damage you're doing
                if self.tonicActive:
                    hitValue -= 5
                    self.tonicActive = False
                
                # Decrement the character's health value
                self.character["HP"] -= hitValue

            # Update the character's health bar
            self.characterHealthBar.updateHealthValue(self.character["HP"])

            # Perofmr the enemy's attack animation
            self.enemySprite.selectAnimation("Attack", True, True)

            # Take action based off of the character's remaining health value
            if (self.character["HP"] <= 0):
                # Use an Auto-Revive if the character has one in their inventory
                if (itemIsInInventory(self.character["inventory"], "Auto-Revive")):
                    for item in self.character["inventory"]:
                        if item["name"] == "Auto-Revive":
                            self.character["inventory"].remove(item)
                            break

                    self.character["HP"] += self.character["maxHealth"]
                    self.characterHealthBar.updateHealthValue(self.character["HP"])
                    self.autoReviveWasUsed = True
                    self.characterSprite.selectAnimation("Hit", True, True)
                # Otherwise, play the Death animation  
                else:
                    self.characterSprite.selectAnimation("Death", True, False)
            else:
                if not self.defenseBuffActive:
                    self.characterSprite.selectAnimation("Hit", True, True)
                else:
                    self.defenseBuffActive = False
    #------------------------------#

    #------------------------------#
    # Function that ends the battle by emitting a signal to the parent Game Object
    def endBattle(self, _):
        if self.enemy["HP"] <= 0:
            if (self.isBossFight):
                self.emitSignal(msg="boss-defeated", data="success", targetID=self.parentID)
            else:
                self.emitSignal(msg="battle-over", data="success", targetID=self.parentID)
        if self.character["HP"] <= 0:
            self.emitSignal(msg="battle-over", data="failure", targetID=self.parentID)
    #------------------------------#

    #------------------------------#
    # Function that is called after a user answers the question in the question modal
    def resultDetermined(self, result):
        self.closeQuestionModal(None)

        if self.turn == "character":
            if (result):
                self.registerQuestionResult(result)
                self.increaseUserScore(self.currentQuestionScore)
                self.performAttack(attacker="character")

                self.showBattleInfoWindow(info="Action Succeeded!", nextAction="end-character-turn")
            elif (not result and self.secondChanceActive):
                self.secondChanceActive = False
                self.showBattleInfoWindow(info="Second Chance Used!", nextAction="rerun-character-question")
            else:
                self.registerQuestionResult(result)

                self.showBattleInfoWindow(info="Attack Failed!", nextAction="show-feedback-window")
            return

        if self.turn == "enemy":
            if (not result):
                if (not self.secondChanceActive):
                    self.performAttack(attacker="enemy")
                    self.registerQuestionResult(result)

                if (self.righteousDefenseActive):
                    self.righteousDefenseActive = False
                    self.showBattleInfoWindow(info="Block Failed!", nextAction="show-righteous-defense-window")
                elif (self.secondChanceActive):
                    self.secondChanceActive = False
                    self.showBattleInfoWindow(info="Second Chance Used!", nextAction="rerun-question")
                elif (self.autoReviveWasUsed):
                    self.autoReviveWasUsed = False
                    self.showBattleInfoWindow(info="Block Failed!", nextAction="show-auto-revive-window")
                else:
                    self.showBattleInfoWindow(info="Block Failed!", nextAction="show-feedback-window")
            else:
                self.registerQuestionResult(result)
                self.increaseUserScore(self.currentQuestionScore)

                self.showBattleInfoWindow(info="Block Succeeded!", nextAction="end-enemy-turn")
            return
    #------------------------------#

    #------------------------------#
    # Function that enables the buttons in the battle interface
    def enableButtons(self):
        for element in self.interfaceElements:
                if element["name"] == "attackOption" or element["name"] == "specialOption" or element["name"] == "itemsOption":
                    element["rect"].enable()
    #------------------------------#

    #------------------------------#
    # Function that disables the buttons in the battle interface
    def disableButtons(self):
        for element in self.interfaceElements:
                if element["name"] == "attackOption" or element["name"] == "specialOption" or element["name"] == "itemsOption":
                    element["rect"].disable()
    #------------------------------#

    #------------------------------#
    # Function that closes the question modal
    def closeQuestionModal(self, _):
        if self.turn == "character":
            self.removeSignalListenerBySourceID(self.questionModal.getGameObjectID())
            self.questionModal.__del__()
            self.questionModal = None
        else:
            self.removeSignalListenerBySourceID(self.enemyQuestionModal.getGameObjectID())
            self.enemyQuestionModal.__del__()
            self.enemyQuestionModal = None

        self.enableButtons()
    #------------------------------#

    #------------------------------#
    # Function that shows the special abilities window over top of the Battle Options
    def showSpecialAbilitiesWindow(self):
        self.specialAbilitiesWindow = SpecialAbilitiesWindow(300, SCREEN_HEIGHT-190, SCREEN_WIDTH-310, 180, disallowedAbilities=self.disallowedAbilities, parentID=self.gameObjectID)
        specialAbilitiesWindowID = self.specialAbilitiesWindow.getGameObjectID()
        self.setSignalListener(msg="use-special-ability", sourceID=specialAbilitiesWindowID, callback=self.useSpecialAbility)
        self.setSignalListener(msg="close-window", sourceID=specialAbilitiesWindowID, callback=self.hideSpecialAbilitiesWindow)
        self.disableButtons()
    #------------------------------#

    #------------------------------#
    # Function that hides the special abilities window
    def hideSpecialAbilitiesWindow(self, _):
        self.removeSignalListenerBySourceID(self.specialAbilitiesWindow.getGameObjectID())
        self.specialAbilitiesWindow.__del__()
        self.specialAbilitiesWindow = None
        self.enableButtons()
    #------------------------------#

    #------------------------------#
    # Function that is called when the user selects a special ability to use
    def useSpecialAbility(self, ability):
        if ability == "Flee":
            # If the room is not a Boss Room, conduct a dice roll to see if they'll successfully flee or not
            if (not self.isBossFight):
                possibilities = [True, False]
                fleeWasSuccessful = random.choices(possibilities, [0.6, 0.4])[0]

                if (fleeWasSuccessful):
                   self.showBattleInfoWindow(info="Action Succeeded!", nextAction="flee-battle")
                else:
                    self.showBattleInfoWindow(info="Action Failed!", nextAction="end-character-turn")
            else:
                self.showBattleInfoWindow(info="Can't Flee from Boss Fight!", nextAction="end-character-turn")

            # Remove "Flee" from their Special Abilities list
            self.disallowedAbilities.append("Flee")
        elif ability == "Righteous Defense" or ability == "Second Chance" or ability == "Sneak Attack":
            # Subtract one from the number of remaining uses of the character's special ability
            character = self.getGlobalDictValue("character")
            specialAbility = character["type"]["specialAbility"]
            specialAbility["uses"] -= 1

            if ability == "Righteous Defense":
                self.righteousDefenseActive = True
            elif ability == "Second Chance":
                self.secondChanceActive = True
            elif ability == "Sneak Attack":
                self.sneakAttackActive = True
                self.performAttack(attacker="character")
                self.showBattleInfoWindow(info="Sneak Attack Used!", nextAction="end-character-turn")
            
            if not ability == "Sneak Attack":
                self.showBattleInfoWindow(info="Action Succeeded!", nextAction="end-character-turn")

        self.hideSpecialAbilitiesWindow(None)
    #------------------------------#

    #------------------------------#
    # Function that shows the items window over top of the Battle Options
    def showItemsWindow(self):
        self.itemsWindow = ItemsWindow(300, SCREEN_HEIGHT-190, SCREEN_WIDTH-310, 180, parentID=self.gameObjectID)
        itemsWindowID = self.itemsWindow.getGameObjectID()
        self.setSignalListener(msg="use-item", sourceID=itemsWindowID, callback=self.useItem)
        self.setSignalListener(msg="close-window", sourceID=itemsWindowID, callback=self.hideItemsWindow)
        self.disableButtons()
    #------------------------------#

    #------------------------------#
    # Function that hides the items window
    def hideItemsWindow(self, _):
        self.removeSignalListenerBySourceID(self.itemsWindow.getGameObjectID())
        self.itemsWindow.__del__()
        self.itemsWindow = None
        self.enableButtons()
    #------------------------------#

    #------------------------------#
    # Function that is called when a user selects an item to use
    def useItem(self, itemType):
        actuallyUseItem = True

        # Apply the appropriate item effect
        if itemType == "Potion":
            if self.character["HP"] < 100:
                if self.character["HP"] + 30 > 100:
                    self.character["HP"] = 100
                else:
                    self.character["HP"] += 30
                self.characterHealthBar.updateHealthValue(self.character["HP"])
            else:
                actuallyUseItem = False
        if itemType == "Elixir":
            # Add one usage to the character's special ability
            if self.character["type"]["specialAbility"]["uses"] < 3:
                self.character["type"]["specialAbility"]["uses"] += 1
            else:
                actuallyUseItem = False
        if itemType == "Bomb":
            if self.enemy["HP"] - 30 < 0:
                self.enemy["HP"] = 0
            else:
                self.enemy["HP"] -= 30

            self.enemyHealthBar.updateHealthValue(self.enemy["HP"])

            if (self.enemy["HP"] == 0):
                self.enemySprite.selectAnimation("Death", True, False)
            else:
                self.enemySprite.selectAnimation("Hit", True, True)
        if itemType == "Knife":
            if self.enemy["HP"] - 10 < 0:
                self.enemy["HP"] = 0
            else:
                self.enemy["HP"] -= 10

            self.enemyHealthBar.updateHealthValue(self.enemy["HP"])

            if (self.enemy["HP"] == 0):
                self.enemySprite.selectAnimation("Death", True, False)
            else:
                self.enemySprite.selectAnimation("Hit", True, True)
        if itemType == "Stimulant":
            self.stimulantActive = True
            self.stimulantTurnsleft = 2
        if itemType == "Tonic":
            if self.righteousDefenseActive:
                actuallyUseItem = False
            else:
                self.tonicActive = True

        # Remove one instance of the specified item from the user's inventory if they actually used it
        if actuallyUseItem:
            inventory = self.character["inventory"]

            for item in inventory:
                if item["name"] == itemType:
                    inventory.remove(item)
                    break

        # Close the items window
        self.hideItemsWindow(None)

        self.showBattleInfoWindow(info="Action Succeeded!", nextAction="end-character-turn")
    #------------------------------#

    #------------------------------#
    # Function that ends the current turn and effectively transfers control to the other actor    
    def endTurn(self):
        if (self.turn == "character"):
            self.disableButtons()
            self.turn = "enemy"
            self.turnIndicatorText.__del__()
            indicatorText = "Enemy Turn"
            indicatorTextWidth, indicatorTextHeight = self.optionsFont.size(indicatorText)
            textX = SCREEN_WIDTH//2 - indicatorTextWidth//2
            textY = 10
            self.turnIndicatorText = SimpleText(text="Enemy Turn", fontSize=MED_FONT_SIZE, x=textX, y=textY)

            self.showBattleInfoWindow(info="Enemy turn starting!", nextAction="start-enemy-turn")
        else:
            self.turn = "character"
            self.turnIndicatorText.__del__()
            indicatorText = "Character Turn"
            indicatorTextWidth, indicatorTextHeight = self.optionsFont.size(indicatorText)
            textX = SCREEN_WIDTH//2 - indicatorTextWidth//2
            textY = 10
            self.turnIndicatorText = SimpleText(text="Character Turn", fontSize=MED_FONT_SIZE, x=textX, y=textY)

            self.showBattleInfoWindow(info="Character turn starting!", nextAction="start-character-turn")
    #------------------------------#

    #------------------------------#
    # Function that runs the enemy turn      
    def runEnemyTurn(self, questionInfo=None):
        # Get a random question from the Game Engine if no default info was provided
        if (questionInfo == None):
            questionInfo = self.getQuestion(self.roomDifficulty)

        question = questionInfo["Question"]
        answer = questionInfo["Answer"]
        questionType = questionInfo["type"]
        self.currentQuestionInfo = questionInfo
        self.currentQuestionFeedback = questionInfo["Feedback"] if questionInfo["Feedback"] != None else "No feedback"
        self.currentQuestionScore = questionInfo["score"]

        # Spawn different types of question modals based on the question type and set signal listeners
        if questionType == "multiple-choice":
            self.enemyQuestionModal = MultipleChoiceQuestionModal(centerX=SCREEN_WIDTH//2, centerY=SCREEN_HEIGHT//2-100, width=800, height=600, question=question, answer=answer, questionInfo=questionInfo, incorrectAnswers=questionInfo["incorrectAnswers"].copy(), parentID=self.gameObjectID)
        else:
            self.enemyQuestionModal = QuestionModal(centerX=SCREEN_WIDTH//2, centerY=SCREEN_HEIGHT//2-100, width=800, height=600, question=question, answer=answer, questionInfo=questionInfo, parentID=self.gameObjectID)

        enemyQuestionModalID = self.enemyQuestionModal.getGameObjectID()
        self.setSignalListener(msg="result-determined", sourceID=enemyQuestionModalID, callback=self.enemyResultDetermined)
        self.setSignalListener(msg="close-modal", sourceID=enemyQuestionModalID, callback=self.skippedEnemyQuestion)
    #------------------------------#

    #------------------------------#
    # Function that is called when the result has been determined for the question the enemy asks the player
    def enemyResultDetermined(self, result):
        self.resultDetermined(result)
    #------------------------------#

    #------------------------------#
    # Function that is called when the player skips the enemy's question
    def skippedEnemyQuestion(self, _):
        self.closeQuestionModal(None)
        self.performAttack(attacker="enemy")

        if (self.righteousDefenseActive):
            self.righteousDefenseActive = False
            self.showBattleInfoWindow(info="Block Failed!", nextAction="show-righteous-defense-window")
        else:
            self.showBattleInfoWindow(info="Block Failed!", nextAction="show-feedback-window")
    #------------------------------#

    #------------------------------#
    # Function that is called when the feedback window is closed   
    def feedbackWindowClosed(self, _):
        self.removeSignalListenerBySourceID(self.feedbackWindow.getGameObjectID())
        self.feedbackWindow.__del__()
        self.endTurn()
    #------------------------------#

    #------------------------------#
    # Function that shows the Battle Info Window
    def showBattleInfoWindow(self, info, nextAction):
        self.disableButtons()

        self.battleInfoWindow = BattleInfoWindow(info=info, callbackArg=nextAction, parentID=self.gameObjectID)
        self.setSignalListener(msg="close", sourceID=self.battleInfoWindow.getGameObjectID(), callback=self.closeBattleInfoWindow)
    #------------------------------#

    #------------------------------#
    # Function that closes the Battle Info Window   
    def closeBattleInfoWindow(self, nextAction):
        self.removeSignalListenerBySourceID(self.battleInfoWindow.getGameObjectID())
        self.battleInfoWindow.__del__()

        if nextAction == "show-feedback-window":
            self.feedbackWindow = FeedbackWindow(title="Feedback:", feedback=self.currentQuestionFeedback, parentID=self.gameObjectID)
            self.setSignalListener(msg="close", sourceID=self.feedbackWindow.getGameObjectID(), callback=self.feedbackWindowClosed)
        elif nextAction == "start-enemy-turn":
            self.runEnemyTurn()
        elif nextAction == "start-character-turn":
            self.enableButtons()
        elif nextAction == "end-character-turn":
            self.endTurn()
        elif nextAction == "end-enemy-turn":
            self.endTurn()
        elif nextAction == "flee-battle":
            self.fleeBattle()
        elif nextAction == "show-righteous-defense-window":
            self.showBattleInfoWindow(info="Righteous Defense used!", nextAction="show-feedback-window")
        elif nextAction == "rerun-question":
            self.runEnemyTurn(questionInfo=self.currentQuestionInfo)
        elif nextAction == "rerun-character-question":
            self.optionSelected(option="attack", defaultQuestionInfo=self.currentQuestionInfo)
        elif nextAction == "show-auto-revive-window":
            self.showBattleInfoWindow(info="Auto-Revive used!", nextAction="show-feedback-window")
    #------------------------------#

    #------------------------------#
    # Function that emits a signal to the parent to flee the battle        
    def fleeBattle(self):
        self.emitSignal(msg="flee-battle", data="flee", targetID=self.parentID)
    #------------------------------#
import pygame
from engine_initialization import GameEngine
from .game_object import GameObject
from .interactive_rect import InteractiveRect
from utils import *
from constants import *

class Textbox(GameObject):
    #------------------------------#
    # Constructor Function
    def __init__(self, TLx, TLy, maxCharacters=30, width=0, height=0, parentID="", zIndex=0):
        self.parentID = parentID
        super().__init__(zIndex=zIndex)
        self.regularFont = pygame.font.Font(GAME_FONT_PATH, REG_FONT_SIZE)
        self.TLx = TLx
        self.TLy = TLy
        self.userInputString = ""
        self.submitted = False
        self.maxCharacters = maxCharacters

        characterWidth, characterHeight = self.regularFont.size("A")
        
        if width == 0:
            self.width = characterWidth * self.maxCharacters
        else:
            self.width = width

        if height == 0:
            self.height = characterHeight + 8
        else:
            self.height = height

        self.rectangle = None
        self.userTextSurface = None

        self.renderCursor = True

        self.initializeElements()
    #------------------------------#

    #------------------------------#
    # Destructor Function
    def __del__(self):
        if self.rectangle != None:
            self.rectangle.__del__()
        super().__del__()
    #------------------------------#

    #------------------------------#
    # Function that updates the Textbox
    def update(self, frameCounter, deltaTime):
        if frameCounter >= 0 and frameCounter < 30:
            self.renderCursor = True
        else:
            self.renderCursor = False
    #------------------------------#

    #------------------------------#
    # Function that renders the game object
    def render(self, canvas):
        if self.rectangle != None:
            user_input_text_surface = self.regularFont.render(self.userInputString, True, WHITE)
            canvas.blit(user_input_text_surface, (self.TLx + 5, self.TLy + 4))

            if self.renderCursor:
                cursorWidth, cursorHeight = self.regularFont.size("I")
                cursorTLx = self.TLx + 5 + user_input_text_surface.get_width() + 1
                cursorTLy = self.TLy + 4

                cursorRect = pygame.Rect(cursorTLx, cursorTLy, cursorWidth, cursorHeight)
                pygame.draw.rect(canvas, WHITE, cursorRect)
    #------------------------------#

    #------------------------------#
    # Function that handles interaction
    def handleInteraction(self, event, action, mousePos):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                return
            if event.key == pygame.K_DOWN:
                return
            if event.key == pygame.K_LEFT:
                return
            if event.key == pygame.K_RIGHT:
                return
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                self.emitSignal("submitted", self.userInputString, self.parentID);
                return
            if event.key == pygame.K_ESCAPE:
                return
            if event.key == pygame.K_BACKSPACE:
                self.userInputString = self.userInputString[:-1]
                return
            
            if (len(self.userInputString) < self.maxCharacters):
                self.userInputString += event.unicode
    #------------------------------#
    
    #------------------------------#
    # Function that initializes the textbox's elements
    def initializeElements(self):
        self.rectangle = InteractiveRect(self.TLx, self.TLy, self.width, self.height, outlineOnly=True, defaultColor=WHITE, highlightColor=WHITE, text=None, parentID=self.gameObjectID)
    #------------------------------#

    #------------------------------#
    # Function that determines whether the game object was clicked
    def wasClicked(self, mousePos):
        if self.element.collidepoint(mousePos):
            return True
        return False
    #------------------------------#
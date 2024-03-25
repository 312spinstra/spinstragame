import pygame
from .game_object import GameObject
from constants import *
from utils import prepareTextForRendering

# Class that implements a textarea input
class Textarea(GameObject):
    #------------------------------#
    # Constructor function
    def __init__(self, TLx, TLy, width, height, backgroundColor=BLACK, borderColor=WHITE, parentID="", zIndex=0):
        super().__init__(zIndex=zIndex)
        self.parentID = parentID
        self.TLx = TLx
        self.TLy = TLy
        self.width = width
        self.height = height
        self.backgroundColor = backgroundColor
        self.borderColor = borderColor
        self.userInputString = ""
        self.textRows = []
        self.rects = []
        self.renderCursor = True
        self.font = pygame.font.Font(GAME_FONT_PATH, REG_FONT_SIZE)
    #------------------------------#

    #------------------------------#
    # Function that initializes the rectangles used to draw the textarea background
    def initializeRects(self):
        mainRect = pygame.Rect(self.TLx, self.TLy, self.width, self.height)
        self.rects.append({"name": "mainRect", "rect": mainRect})
        borderRect = pygame.Rect(self.TLx, self.TLy, self.width, self.height)
        self.rects.append({"name": "borderRect", "rect": borderRect})
    #------------------------------#

    #------------------------------#
    # Function that updates the Textarea
    def update(self, frameCounter, deltaTime):
        if frameCounter >= 0 and frameCounter < 30:
            self.renderCursor = True
        else:
            self.renderCursor = False
    #------------------------------#

    #------------------------------#
    # Function that renders the textarea on the canvas
    def render(self, canvas):
        if len(self.rects) == 0:
            self.initializeRects()

        for rect in self.rects:
            if rect["name"] == "mainRect":
                pygame.draw.rect(canvas, self.backgroundColor, rect["rect"])
            else:
                pygame.draw.rect(canvas, self.borderColor, rect["rect"], 2)

        if len(self.userInputString) > 0:
            self.textRows = prepareTextForRendering(self.userInputString, REG_FONT_SIZE, self.width-10)

        lastRowX = -1
        lastRowY = -1

        for index, row in enumerate(self.textRows):
                textWidth, textHeight = self.font.size(row)
                row = self.font.render(row, True, WHITE)

                canvas.blit(row, (self.TLx + 5, self.TLy + 5 + ((5 + textHeight) * index)))

                if (index == len(self.textRows) - 1):
                    lastRowX = self.TLx + 5 + textWidth + 1
                    lastRowY = self.TLy + 5 + ((5 + textHeight) * index)

        if self.renderCursor:
            if lastRowX == -1 and lastRowY == -1:
                lastRowX = self.TLx + 5
                lastRowY = self.TLy + 5

            cursorWidth, cursorHeight = self.font.size("I")
            cursorTLx = lastRowX
            cursorTLy = lastRowY

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
            
            self.userInputString += event.unicode
    #------------------------------#
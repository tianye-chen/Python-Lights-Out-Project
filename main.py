import pygame
import random
import time

pygame.init()
pygame.display.set_caption('Lights Out')

# Keeps tracks of steps taken by the player
numSteps = 0
# Displays numSteps onto the screen
numStepsText = (pygame.font.Font('freesansbold.ttf', 32)).render('Steps: '+(str(numSteps)), True, [0,0,0])
# The puzzle is solved when allGreen is true
allGreen = False
# Contains all the gameBlocks in the puzzle
blockList = []
# Width and height of the blockList
width = 3
height = 3

# Each of block of either green or red is an object of this class
# The block will be green if blockState = 1
# The block will be red if blockState = 0
class gameBlock():
    def __init__(self, blockState, locX, locY):
        self.blockState = blockState
        self.locX = locX
        self.locY = locY

    def flip(self):
        self.blockState = not(self.blockState)

    def getCoords(self):
        return [self.locX, self.locY]

    def getState(self):
        return self.blockState

    def isWithin(self, otherX, otherY):
        if self.locX <= otherX and self.locY <= otherY and self.locX + 50 >= otherX and self.locY + 50 >= otherY:
            return True
        else: 
            return False

# Draws all the gameBlocks from blockList onto the screen
def drawAllBlock(blockList, screen):
    global allGreen
    allGreen = True
    for innerList in blockList:
        for block in innerList:
            if (block.getState()):
                color = [0,255,0]
            else:
                color = [255,0,0]
                allGreen = False
            coords = block.getCoords()
            pygame.draw.rect(screen, [0,0,0], (coords[0]-2, coords[1]-2, 53, 53), 2)
            pygame.draw.rect(screen,color, (coords[0], coords[1], 50, 50))
    return allGreen

# Flips all the adjacent gameBlocks into the other color
def flipAllAdjacent(i,j):
    global blockList
    blockList[i][j].flip() # center
    if i + 1 < len(blockList): blockList[i+1][j].flip() # bottom
    if i - 1 != -1: blockList[i-1][j].flip() # top
    if j + 1 < len(blockList[i]): blockList[i][j+1].flip() # right
    if j - 1 != -1: blockList[i][j-1].flip() # left
    global numSteps
    numSteps += 1
    global numStepsText
    numStepsText = (pygame.font.Font('freesansbold.ttf', 32)).render('Steps: '+(str(numSteps)), True, [0,0,0])

# Generates and returns random 2d list of gameBlocks randomized with either 0 or 1
def setBoard(scWidth, scHeight, width, height):
    return [[(gameBlock(random.randint(0,1), ((scWidth/2)-width*27)+(j*50)+j*6, (scHeight/2-height*27)+(i*50)+i*6)) for j in range(width)] for i in range(height)]

# Draws the clickable buttons onto the screen
def drawButtons(screen, resetButton, scHeight, scWidth):
    pygame.draw.rect(screen, [150,150, 150], resetButton)
    pygame.draw.polygon(screen, [0,0,0], [[285,scHeight-25], [275,scHeight-15], [295, scHeight-15]])
    pygame.draw.polygon(screen, [0,0,0], [[373,scHeight-15], [363,scHeight-25], [383, scHeight-25]])
    pygame.draw.polygon(screen, [0,0,0], [[135,scHeight-25], [125,scHeight-15], [145, scHeight-15]])
    pygame.draw.polygon(screen, [0,0,0], [[233,scHeight-15], [223,scHeight-25], [243, scHeight-25]])

# Automatically solves the puzzle (Work in Progress)
def autoSolve():
    global width
    global height
    global blockList
    blockCoordX = random.randint(0,height-1)
    blockCoordY = random.randint(0,width-1)
    while (blockList[blockCoordX][blockCoordY].getState() != 0):
        blockCoordX = random.randint(0,height-1)
        blockCoordY = random.randint(0,width-1)
    flipAllAdjacent(blockCoordX, blockCoordY)


def main():
    isRunning = True
    isSolving = False
    global width
    global height
    scWidth = 800
    scHeight = 600
    screen = pygame.display.set_mode([scWidth, scHeight])
    screen.fill([255,255,255])


    global numSteps
    numSteps = 0
    global numStepsText
    numStepsText = (pygame.font.Font('freesansbold.ttf', 32)).render('Steps: '+(str(numSteps)), True, [0,0,0])
    global blockList
    blockList = setBoard(scWidth, scHeight, width, height)
    global allGreen

    resetButtonText = (pygame.font.Font('freesansbold.ttf', 32)).render('Reset', True, [255,0,0])
    resetButton = pygame.draw.rect(screen, [150,150,150], (0, scHeight-32, 90, 40))
    widthText = (pygame.font.Font('freesansbold.ttf', 32)).render('W: '+str(width), True, [0,0,0])
    widthUp = pygame.draw.polygon(screen, [0,0,0], [[135,scHeight-25], [125,scHeight-15], [145, scHeight-15]])
    widthDown = pygame.draw.polygon(screen, [0,0,0], [[233,scHeight-15], [223,scHeight-25], [243, scHeight-25]])
    heightText = (pygame.font.Font('freesansbold.ttf', 32)).render('H: '+str(height), True, [0,0,0])
    heightUp = pygame.draw.polygon(screen, [0,0,0], [[285,scHeight-25], [275,scHeight-15], [295, scHeight-15]])
    heightDown = pygame.draw.polygon(screen, [0,0,0], [[373,scHeight-15], [363,scHeight-25], [383, scHeight-25]])
    solveButtonText = (pygame.font.Font('freesansbold.ttf', 32)).render('Solve (WIP)', True, [255,0,0])
    solvetButton = pygame.draw.rect(screen, [150,150,150], (scWidth-180, scHeight-32, 90, 40))

    drawAllBlock(blockList,screen)

    while isRunning:
        if isSolving and not allGreen:
            autoSolve()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False
            # Looks for a click on any clickable object on the screen
            elif event.type == pygame.MOUSEBUTTONUP and not allGreen:
                # gameBlock
                for i in range(height):
                    for j in range(width):
                        if blockList[i][j].isWithin(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]):
                            flipAllAdjacent(i,j)
                # Reset Button
                if resetButton.collidepoint(pygame.mouse.get_pos()):
                    numSteps = 0
                    numStepsText = (pygame.font.Font('freesansbold.ttf', 32)).render('Steps: '+str(numSteps), True, [0,0,0])
                    blockList = setBoard(scWidth, scHeight, width, height)
                # gameList Width incrementer
                if widthUp.collidepoint(pygame.mouse.get_pos()):
                    width += 1
                    blockList = setBoard(scWidth, scHeight, width, height)
                    widthText = (pygame.font.Font('freesansbold.ttf', 32)).render('W: '+str(width), True, [0,0,0])
                # blockList width decrementer
                if widthDown.collidepoint(pygame.mouse.get_pos()):
                    width -= 1
                    blockList = setBoard(scWidth, scHeight, width, height)
                    widthText = (pygame.font.Font('freesansbold.ttf', 32)).render('W: '+str(width), True, [0,0,0])
                # blockList height incrementer
                if heightUp.collidepoint(pygame.mouse.get_pos()):
                    height += 1
                    blockList = setBoard(scWidth, scHeight, width, height)
                    heightText = (pygame.font.Font('freesansbold.ttf', 32)).render('H: '+str(height), True, [0,0,0])
                # blockList height decrementer
                if heightDown.collidepoint(pygame.mouse.get_pos()):
                    height -= 1
                    blockList = setBoard(scWidth, scHeight, width, height)
                    heightText = (pygame.font.Font('freesansbold.ttf', 32)).render('H: '+str(height), True, [0,0,0])
                # Solve button
                if solvetButton.collidepoint(pygame.mouse.get_pos()):
                    isSolving = not isSolving
                    if isSolving:
                        solveButtonText = (pygame.font.Font('freesansbold.ttf', 32)).render('Solve (WIP)', True, [0,255,0])
                    else:
                        solveButtonText = (pygame.font.Font('freesansbold.ttf', 32)).render('Solve (WIP)', True, [255,0,0])
            # Prevents interaction with any button other than Reset when the puzzle is solved
            elif event.type == pygame.MOUSEBUTTONUP:
                if resetButton.collidepoint(pygame.mouse.get_pos()):
                    numSteps = 0
                    allGreen = False
                    isSolving = False
                    solveButtonText = (pygame.font.Font('freesansbold.ttf', 32)).render('Solve (WIP)', True, [255,0,0])
                    numStepsText = (pygame.font.Font('freesansbold.ttf', 32)).render('Steps: '+str(numSteps), True, [0,0,0])
                    blockList = setBoard(scWidth, scHeight, width, height)
        # Refreshes and displays all the elements onto the screen
        screen.fill([255,255,255])
        drawButtons(screen, resetButton, scHeight, scWidth)
        screen.blit(resetButtonText, (0, scHeight-32))
        screen.blit(widthText, (150, scHeight-32))
        screen.blit(heightText, (300, scHeight-32))
        screen.blit(numStepsText, (0,0))
        screen.blit(solveButtonText, (scWidth-180, scHeight-32))
        allGreen = drawAllBlock(blockList, screen)
        pygame.display.flip()
            
main()


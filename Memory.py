import pygame
import sys
import time
import random
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 900
WINDOWHEIGHT = 600
FLASHSPEED = 500 # MILISEC
FLASHDELAY= 200 # MILLISEC
BUTTONSIZE = 200
BUTTONGAPSIZE = 30
TIMEOUT = 4 # SEC BEFORE GAME OVER IF NO BUTTON IS PRESSED

# COLORS DEFINING

WHITE = (255,255,255)
BLACK = (0,0,0)
BRIGHTRED = (255,0,0)
RED = (155,0,0)
BRIGHTGREEN = (0,255,0)
GREEN = (0,155,0)
BRIGHTBLUE = (0,0,255)
BLUE = (0,0,155)
BRIGHTYELLOW = (255,255,0)
YELLOW = (155,155,0)
DARKGRAY= (40,40,40)
bgColor = BLACK

STARTBUTTON= pygame.Rect(370,520,160,40)
RESTARTBUTTON = pygame.Rect(540,520,160,40)

XMARGIN = int((WINDOWWIDTH - (2*BUTTONSIZE)-BUTTONGAPSIZE)/2)
YMARGIN = int((WINDOWHEIGHT-(2*BUTTONSIZE)-BUTTONGAPSIZE)/2)

# RECT OBJECTS FOR ALL 4 BUTTON

YELLOWRECT = pygame.Rect(XMARGIN,YMARGIN,BUTTONSIZE,BUTTONSIZE)
BLUERECT = pygame.Rect(XMARGIN + BUTTONSIZE+ BUTTONGAPSIZE, YMARGIN, BUTTONSIZE, BUTTONSIZE)
GREENRECT = pygame.Rect(XMARGIN+BUTTONSIZE+BUTTONGAPSIZE, YMARGIN+BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)
REDRECT = pygame.Rect(XMARGIN,YMARGIN + BUTTONSIZE + BUTTONGAPSIZE , BUTTONSIZE, BUTTONSIZE)

def main():
    global FPSCLOCK , DISPLAYSURF , BASICFONT 

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Memory Rushh')
    BASICFONT = pygame.font.Font('freesansbold.ttf',16)
    infoSurf = BASICFONT.render('Match the pattern by clicking on button or using the Q,W,A,S keys',1,DARKGRAY)
    infoRect = infoSurf.get_rect()
    infoRect.topleft = (10, WINDOWHEIGHT -25)

    pattern =[] # stores pattern
    currentStep = 0 # color the player muct push next
    lastClickTime = 0 # timestamp of players button
    score = 0
    waitingForInput = False 
    while True: # main game loop 
        clickedButton = None 
        DISPLAYSURF.fill(bgColor)
        drawButtons()

        pygame.draw.rect(DISPLAYSURF,GREEN,STARTBUTTON)
        pygame.draw.rect(DISPLAYSURF,BLUE,RESTARTBUTTON)

        startSurf = BASICFONT.render("Start Game",True,WHITE)
        restartSurf = BASICFONT.render("Restart",True,WHITE)

        scoreSurf = BASICFONT.render('Score: ' + str(score),1,WHITE)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (WINDOWWIDTH - 100,10)
        DISPLAYSURF.blit (scoreSurf , scoreRect)
        DISPLAYSURF.blit(infoSurf , infoRect)

        checkForQuit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                mousex , mousey = event.pos
                clickedButton = getButtonClicked(mousex , mousey)
            elif event.type == KEYDOWN:
                if event.key == K_q:
                    clickedButton = YELLOW
                elif event.key == K_w:
                    clickedButton = BLUE
                elif event.key == K_a:
                    clickedButton =RED
                elif event.key == K_s:
                    clickedButton = GREEN

        if not waitingForInput:
            # play pattern
            pygame.display.update()
            pygame.time.wait(1000)
            pattern.append(random.choice((YELLOW,BLUE,RED,GREEN)))
            for button in pattern :
                flashButtonAnimation(button)
                pygame.time.wait(FLASHDELAY)
            waitingForInput = True
        else:
            # w8 for player to enter
            if clickedButton and clickedButton == pattern[currentStep]:
                # pushed correct button
                flashButtonAnimation(clickedButton)
                currentStep += 1
                lastClickTime = time.time()

                if currentStep == len(pattern):
                    # pused last button in pattern
                    changeBackgroundAnimation()
                    score += 1
                    waitingForInput = False
                    currentStep = 0 # reset back to 1st step

            elif (clickedButton and clickedButton != pattern[currentStep]) or (currentStep != 0 and time.time() - TIMEOUT> lastClickTime):
                # wrong or timeout 
                gameOverAnimation()
                # reset variable for new game:
                pattern = []
                currentStep = 0
                waitingForInput = False
                score = 0
                pygame.time.wait(1000)
                changeBackgroundAnimation()

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def terminate():
    pygame.quit()
    sys.exit()

def checkForQuit():
    for event in pygame.event.get(QUIT):# get all quit events
        terminate() # if any QUIT events r there
    for event in pygame.event.get(KEYUP): # get all keyup events
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)        

def flashButtonAnimation(color , animationSpeed=50):
    if color == YELLOW:
        flashColor = BRIGHTYELLOW
        rectangle = YELLOWRECT
    elif color == BLUE:
        flashColor = BRIGHTBLUE
        rectangle = BLUERECT
    elif color == RED:
        flashColor = BRIGHTRED
        rectangle = REDRECT
    elif color == GREEN:
        flashColor = BRIGHTGREEN
        rectangle = GREENRECT            

    origSurf = DISPLAYSURF.copy()
    flashSurf = pygame.Surface((BUTTONSIZE , BUTTONSIZE))
    flashSurf = flashSurf.convert_alpha()
    r , g, b = flashColor
    for start , end, step in ((0,255,1),(255,0,-1)):# animation loop
        for alpha in range(start, end , animationSpeed*step):
            checkForQuit()
            DISPLAYSURF.blit(origSurf,(0,0))
            flashSurf.fill((r,g,b, alpha))
            DISPLAYSURF.blit(flashSurf, rectangle.topleft)
            pygame.display.update()
            FPSCLOCK.tick(FPS)
            DISPLAYSURF.blit(origSurf,(0,0))

def drawButtons():
    pygame.draw.rect(DISPLAYSURF,YELLOW,YELLOWRECT)
    pygame.draw.rect(DISPLAYSURF,BLUE,BLUERECT)
    pygame.draw.rect(DISPLAYSURF,RED,REDRECT)
    pygame.draw.rect(DISPLAYSURF,GREEN,GREENRECT)

def changeBackgroundAnimation(animationSpeed=40):
    global bgColor
    newBgColor = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    newBgSurf = pygame.Surface((WINDOWWIDTH,WINDOWHEIGHT))
    newBgSurf = newBgSurf.convert_alpha()
    r,g,b = newBgColor
    for alpha in range (0,255,animationSpeed): #animation loop
        checkForQuit()
        DISPLAYSURF.fill(bgColor)

        newBgSurf.fill((r,g,b,alpha))
        DISPLAYSURF.blit(newBgSurf,(0,0))
        drawButtons() # redraw the button on top

        pygame.display.update()
        FPSCLOCK.tick(FPS)
    bgColor = newBgColor

def gameOverAnimation(color=WHITE, animationSpeed=50):
    origSurf=DISPLAYSURF.copy()
    flashSurf = pygame.Surface(DISPLAYSURF.get_size())
    flashSurf = flashSurf.convert_alpha()
    r,g,b= color
    for i in range(3): # all 3 flash
        for start,end,step in((0,255,1),(255,0,-1)):
            for alpha in range(start,end,animationSpeed*step):
                # alpha means transpareny. 255 is opaque, 0 is invisible
                checkForQuit()
                flashSurf.fill((r,g,b,alpha))
                DISPLAYSURF.blit(origSurf,(0,0))
                DISPLAYSURF.blit(flashSurf,(0,0))
                drawButtons()
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def getButtonClicked(x,y):
    if YELLOWRECT.collidepoint((x,y)):
        return YELLOW
    elif BLUERECT.collidepoint((x,y)):
        return BLUE
    elif REDRECT.collidepoint((x,y)):
        return RED
    elif GREENRECT.collidepoint((x,y)):
        return GREEN
    return None                    



if __name__ == '__main__':
    main()








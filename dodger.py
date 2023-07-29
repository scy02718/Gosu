import pygame, random, sys
from pygame.locals import *

WINDOWWIDTH = 1000
WINDOWHEIGHT = 600
TEXTCOLOR = (255, 255, 255)
BACKGROUNDCOLOR = (0, 0, 0)
FPS = 60
BADDIESIZE = 10
BADDIESPEED = 5
ADDNEWBADDIERATE = 2
PLAYERMOVERATE = 7

def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # pressing escape quits
                    terminate()
                return

def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# set up pygame, the window, and the mouse cursor
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Dodger')

# set up fonts
font = pygame.font.SysFont(None, 48)

# set up sounds
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('background.mid')

# set up images
# Custom images -> Arrows, Character, Boss (maybe)
playerImage = pygame.image.load('player.png')
playerRect = playerImage.get_rect()
baddieImage = pygame.image.load('baddie.png')

# show the "Start" screen
drawText('Dodger', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()


topScore = 0
while True:
    # set up the start of the game
    baddies = [] # Saves details of arrows (add new variable named directions)
    score = 0
    playerRect.topleft = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0
    pygame.mixer.music.play(-1, 0.0)

    while True: # the game loop runs while the game part is playing
        score += 1 # increase score

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == ord('z'):
                    reverseCheat = True
                if event.key == ord('x'):
                    slowCheat = True
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                if event.key == ord('z'):
                    reverseCheat = False
                    score = 0
                if event.key == ord('x'):
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                        terminate()

                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False

        # Add new baddies at the top of the screen, if needed.
        # ADDNEWBADDIERATE = rate of arrows coming out -> Change depending on time
        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            # Arrow 크기는 fixed, so do not need this
            # Position of arrow startingcan be anywhere, direction of arrow should be towards the user, not only towards bottom.

            # x, y 를 정해줘야돼
            # x 가 랜덤이면 y = 0 or WINDOWHEIGHT
            # y 가 랜덤이면 x = 0 or WINDOWWIDTH
            # 이거조차도 랜덤으로 해야돼

            side = random.randint(0, 3)
            if side == 0:
                newBaddie = {'rect': pygame.Rect(0 - BADDIESIZE, random.randint(0, WINDOWHEIGHT-BADDIESIZE), BADDIESIZE, BADDIESIZE),
                        'speed': BADDIESPEED,
                        'surface':pygame.transform.scale(baddieImage, (BADDIESIZE, BADDIESIZE)),
                        }
            elif side == 1:
                newBaddie = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH-BADDIESIZE), WINDOWHEIGHT + BADDIESIZE, BADDIESIZE, BADDIESIZE),
                        'speed': BADDIESPEED,
                        'surface':pygame.transform.scale(baddieImage, (BADDIESIZE, BADDIESIZE)),
                        }
            elif side == 2:
                newBaddie = {'rect': pygame.Rect(WINDOWWIDTH + BADDIESIZE, random.randint(0, WINDOWHEIGHT-BADDIESIZE), BADDIESIZE, BADDIESIZE),
                        'speed': BADDIESPEED,
                        'surface':pygame.transform.scale(baddieImage, (BADDIESIZE, BADDIESIZE)),
                        }
            else:
                newBaddie = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH-BADDIESIZE), 0 - BADDIESIZE, BADDIESIZE, BADDIESIZE),
                        'speed': BADDIESPEED,
                        'surface':pygame.transform.scale(baddieImage, (BADDIESIZE, BADDIESIZE)),
                        }

            baddies.append(newBaddie)

        # Move the player around.
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)

        # Move the baddies down.
        # Apply directions later on
        for b in baddies:
            b['rect'].move_ip((playerRect.x - b['rect'].x)*0.01, (playerRect.y - b['rect'].y)*0.01)

         # Delete baddies that have fallen past the other side

        # Draw the game world on the window.
        windowSurface.fill(BACKGROUNDCOLOR)

        # Draw the score and top score.
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)

        # Draw the player's rectangle
        windowSurface.blit(playerImage, playerRect)

        # Draw each baddie
        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])

        pygame.display.update()

        # Check if any of the baddies have hit the player.
        if playerHasHitBaddie(playerRect, baddies):
            if score > topScore:
                topScore = score # set new top score
            break

        mainClock.tick(FPS)

    # Stop the game and show the "Game Over" screen.
    pygame.mixer.music.stop()
    gameOverSound.play()

    drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    drawText('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()

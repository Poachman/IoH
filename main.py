import sys, pygame, pygbutton
pygame.init()
pygame.font.init()

pygame.display.set_caption("Project Internet of Hearts")

size = width, height = 480, 320

view = 1  #which screen we're at

surface     = pygame.display.set_mode(size)
drawCanvas  = pygame.surface.Surface((410,300))

btnSend = pygbutton.PygButton((10,10,width-20,100), 'Send Message', (100,100,100), (0,0,0), pygame.font.Font('freesansbold.ttf', 30))
btnRead = pygbutton.PygButton((10,10 + 110,width-20,100), 'Read Messages', (100,100,100), (0,0,0), pygame.font.Font('freesansbold.ttf', 30))
mainMenuButtons = (btnSend, btnRead)

btnColorBlue    = pygbutton.PygButton((10, 10      , 40, 40), '', (  0,   0, 255), (0,0,0))
btnColorRed     = pygbutton.PygButton((10, 14 +  40, 40, 40), '', (255,   0,   0), (0,0,0))
btnColorGreen   = pygbutton.PygButton((10, 18 +  80, 40, 40), '', (  0, 255,   0), (0,0,0))
btnColorYellow  = pygbutton.PygButton((10, 22 + 120, 40, 40), '', (  0, 255, 255), (0,0,0))
btnColorOrange  = pygbutton.PygButton((10, 26 + 160, 40, 40), '', (255, 255,   0), (0,0,0))
btnColorPurple  = pygbutton.PygButton((10, 30 + 200, 40, 40), '', (255,   0, 255), (0,0,0))
btnColorWhite   = pygbutton.PygButton((10, 34 + 240, 40, 40), '', (255, 255, 255), (0,0,0))
colorButtons    = (btnColorPurple, btnColorOrange, btnColorYellow, btnColorRed, btnColorGreen, btnColorBlue, btnColorWhite)

def MainMenu():
    for b in mainMenuButtons:
        b.draw(surface)

def SendMenu():
    for b in colorButtons:
        b.draw(surface)
    surface.blit(drawCanvas, (60,10))

def ReadMenu():
    print "Reading Menu"

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if view == 1:
            if 'click' in btnSend.handleEvent(event):
                view = 2
            if 'click' in btnRead.handleEvent(event):
                view = 3
        if view == 2:
            drawCanvas.fill((255,255,255));

    surface.fill((30,30,30))


    if view == 1:
        MainMenu()
    elif view == 2:
        SendMenu()
    elif view == 3:
        ReadMenu()
    else:
        view = 1

    pygame.display.flip()

import sys, pygame, pygbutton, operator
pygame.init()
pygame.font.init()

pygame.display.set_caption("Project Internet of Hearts")

size = width, height = 480, 320

view = 1  #which screen we're at

canvasColor = (255,255,255)

surface     = pygame.display.set_mode(size)
drawCanvas  = pygame.surface.Surface((410,255))
drawCanvas.fill(canvasColor)

btnSend = pygbutton.PygButton((10,10,width-20,100), 'Send Message', (100,100,100), (0,0,0), pygame.font.Font('freesansbold.ttf', 30))
btnRead = pygbutton.PygButton((10,10 + 110,width-20,100), 'Read Messages', (100,100,100), (0,0,0), pygame.font.Font('freesansbold.ttf', 30))
mainMenuButtons = (btnSend, btnRead)


btnColorBlue    = pygbutton.PygButton((10, 8       , 40, 40), '', (  0,   0, 255), (0,0,0))
btnColorRed     = pygbutton.PygButton((10, 12 +  40, 40, 40), '', (255,   0,   0), (0,0,0))
btnColorGreen   = pygbutton.PygButton((10, 16 +  80, 40, 40), '', (  0, 255,   0), (0,0,0))
btnColorYellow  = pygbutton.PygButton((10, 20 + 120, 40, 40), '', (  0, 255, 255), (0,0,0))
btnColorOrange  = pygbutton.PygButton((10, 24 + 160, 40, 40), '', (255, 255,   0), (0,0,0))
btnColorPurple  = pygbutton.PygButton((10, 28 + 200, 40, 40), '', (255,   0, 255), (0,0,0))
btnColorBlack   = pygbutton.PygButton((10, 32 + 240, 40, 40), '', (  0,   0,   0), (0,0,0))
colorButtons    = (btnColorPurple, btnColorOrange, btnColorYellow, btnColorRed, btnColorGreen, btnColorBlue, btnColorBlack)

btnClearDrawing = pygbutton.PygButton((60, 32 + 240, 40, 40), '', (60, 60, 60), (0,0,0))
btnSendDrawing  = pygbutton.PygButton((60+50, 32 + 240, 40, 40), '', (60, 60, 60), (0,0,0))
sendButtons     = (btnClearDrawing, btnSendDrawing)

def MainMenu():
    for b in mainMenuButtons:
        b.draw(surface)

def SendMenu():
    for b in colorButtons:
        b.draw(surface)
    for b in sendButtons:
        b.draw(surface)
    if pygame.mouse.get_pressed()[0]:
#        print pygame.mouse.get_pos(),  pygame.mouse.get_rel()
        pygame.draw.line(drawCanvas, (0,0,0), map(operator.sub, map(operator.add, pygame.mouse.get_pos(), (-60,-10)), pygame.mouse.get_rel()), map(operator.add, pygame.mouse.get_pos(), (-60,-10)), 5)
    else:
        pygame.mouse.get_rel()
    surface.blit(drawCanvas, (60,10))

def ReadMenu():
    print "Reading Menu"

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if view == 1: # Main Menu
            if 'click' in btnSend.handleEvent(event):
                view = 2  # Send
            if 'click' in btnRead.handleEvent(event):
                view = 3  # Read
        if view == 2: # Send
            if 'click' in btnClearDrawing.handleEvent(event):
                drawCanvas.fill(canvasColor)
            for b in colorButtons:
                if 'click' in b.handleEvent(event):
                    print b


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

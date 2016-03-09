import sys, pygame, pygbutton, operator
pygame.init()
pygame.font.init()

pygame.display.set_caption("Project Internet of Hearts")

size = width, height = 480, 320

view = 1  #which screen we're at

canvasColor = (255,255,255)

surface     = pygame.display.set_mode(size)
drawCanvas  = pygame.surface.Surface((410,260))
drawCanvas.fill(canvasColor)

btnSend = pygbutton.PygButton((10,10,width-20,100), 'Send Message', (100,100,100), (0,0,0), pygame.font.Font('freesansbold.ttf', 30))
btnRead = pygbutton.PygButton((10,10 + 110,width-20,100), 'Read Messages', (100,100,100), (0,0,0), pygame.font.Font('freesansbold.ttf', 30))
mainMenuButtons = (btnSend, btnRead)

BLUE    = (  0,   0, 255)
RED     = (255,   0,   0)
GREEN   = (  0, 255,   0)
CYAN    = (  0, 255, 255)
YELLOW  = (255, 255,   0)
PURPLE  = (255,   0, 255)
BLACK   = (  0,   0,   0)

drawing = False
drawColor = BLACK
drawSelector = 6;

btnColorBlue    = pygbutton.PygButton((10, 8       , 40, 40), '', BLUE, (0,0,0))
btnColorRed     = pygbutton.PygButton((10, 12 +  40, 40, 40), '', RED, (0,0,0))
btnColorGreen   = pygbutton.PygButton((10, 16 +  80, 40, 40), '', GREEN, (0,0,0))
btnColorCyan    = pygbutton.PygButton((10, 20 + 120, 40, 40), '', CYAN, (0,0,0))
btnColorYellow  = pygbutton.PygButton((10, 24 + 160, 40, 40), '', YELLOW, (0,0,0))
btnColorPurple  = pygbutton.PygButton((10, 28 + 200, 40, 40), '', PURPLE, (0,0,0))
btnColorBlack   = pygbutton.PygButton((10, 32 + 240, 40, 40), '', BLACK, (0,0,0))
colorButtons    = (btnColorPurple, btnColorYellow, btnColorCyan, btnColorRed, btnColorGreen, btnColorBlue, btnColorBlack)

#btnBrushSize    = pygbutton.PygButton((60           , 10,  40, 40), 'Size', (60, 60, 60), (0,0,0), pygame.font.Font('freesansbold.ttf', 20))
btnClearDrawing = pygbutton.PygButton((60 +  40 + 10, 8, 100, 35), 'Clear', (100, 100, 100), (0,0,0), pygame.font.Font('freesansbold.ttf', 20))
btnSendDrawing  = pygbutton.PygButton((60 + 140 + 20, 8, 100, 35), 'Send', (100, 100, 100), (0,0,0), pygame.font.Font('freesansbold.ttf', 20))
sendButtons     = (btnClearDrawing, btnSendDrawing)

def MainMenu():
    for b in mainMenuButtons:
        b.draw(surface)

def SendMenu():
    global drawing
    for b in colorButtons:
        b.draw(surface)
    for b in sendButtons:
        b.draw(surface)
    if drawing:
        pygame.draw.line(drawCanvas, drawColor, map(operator.sub, map(operator.add, pygame.mouse.get_pos(), (-60,-50)), pygame.mouse.get_rel()), map(operator.add, pygame.mouse.get_pos(), (-60,-50)), 5)
    if pygame.mouse.get_pressed()[0]:
        pygame.mouse.get_rel()
        drawing = True
    else:
        drawing = False
    pygame.draw.polygon(surface, (196, 196, 196), ((0, (drawSelector * 44) + 15), (20, (drawSelector * 44) + 28), (0, (drawSelector * 44) + 41)))
    surface.blit(drawCanvas, (60,50))

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
            if 'click' in btnColorBlue.handleEvent(event):
                drawSelector = 0
                drawColor = BLUE
            if 'click' in btnColorRed.handleEvent(event):
                drawSelector = 1
                drawColor = RED
            if 'click' in btnColorGreen.handleEvent(event):
                drawSelector = 2
                drawColor = GREEN
            if 'click' in btnColorCyan.handleEvent(event):
                drawSelector = 3
                drawColor = CYAN
            if 'click' in btnColorYellow.handleEvent(event):
                drawSelector = 4
                drawColor = YELLOW
            if 'click' in btnColorPurple.handleEvent(event):
                drawSelector = 5
                drawColor = PURPLE
            if 'click' in btnColorBlack.handleEvent(event):
                drawSelector = 6
                drawColor = BLACK


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

import sys, pygame, pygbutton
pygame.init()
pygame.font.init()

pygame.display.set_caption("Project Internet of Hearts")

size = width, height = 480, 320

view = 1  #which screen we're at

surface = pygame.display.set_mode(size)

btnSend = pygbutton.PygButton((10,10,width-20,100), 'Send Message', (100,100,100), (0,0,0), pygame.font.Font('freesansbold.ttf', 30))
btnRead = pygbutton.PygButton((10,10 + 110,width-20,100), 'Read Messages', (100,100,100), (0,0,0), pygame.font.Font('freesansbold.ttf', 30))
mainMenuButtons = (btnSend, btnRead)



def MainMenu():
    for b in mainMenuButtons:
        b.draw(surface)

def SendMenu():
    print "Sending Menu"

def ReadMenu():
    print "Reading Menu"

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if 'click' in btnSend.handleEvent(event):
            view = 2
        if 'click' in btnRead.handleEvent(event):
            view = 3

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

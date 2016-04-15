import sys, pygame, pygbutton, operator, time, mail, json, os, threading, thread, math, ConfigParser
pygame.init()
pygame.font.init()

config = ConfigParser.ConfigParser()
config.read('settings.cfg')

pygame.display.set_caption("Project Internet of Hearts")

size = width, height = 480, 320

mailer = mail.mail()

timerStarttime = 0
page = 0
image = 0
view = 1  #which screen we're at
jsonData = []

canvasColor = (255,255,255)

flags = 0
if config.getboolean('Env', 'fullscreen'):
    flags = pygame.FULLSCREEN

surface     = pygame.display.set_mode(size, flags)
drawCanvas  = pygame.surface.Surface((410,260))
drawCanvas.fill(canvasColor)

btnSend = pygbutton.PygButton((10, 10      , width-20, 100), 'Send Message',  (100,100,100), (0,0,0), pygame.font.Font('freesansbold.ttf', 30))
btnRead = pygbutton.PygButton((10, 10 + 110, width-20, 100), 'Read Messages', (100,100,100), (0,0,0), pygame.font.Font('freesansbold.ttf', 30))
btnQuit = pygbutton.PygButton((10, 10 + 220, width-20,  80), 'Quit',          (100,100,100), (0,0,0), pygame.font.Font('freesansbold.ttf', 30))
if config.getboolean('Env', 'debug'):
    mainMenuButtons = (btnSend, btnRead, btnQuit)
else:
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
btnBack         = pygbutton.PygButton((60 + 140 + 20, 8, 100, 35), 'Back', (100, 100, 100), (0,0,0), pygame.font.Font('freesansbold.ttf', 20))
btnSendDrawing  = pygbutton.PygButton((60 + 240 + 30, 8, 100, 35), 'Send', (100, 100, 100), (0,0,0), pygame.font.Font('freesansbold.ttf', 20))
sendButtons     = (btnClearDrawing, btnSendDrawing, btnBack)

btnGetMail      = pygbutton.PygButton((60 +  40 + 15, 8, 100, 35), 'Refresh', (100, 100, 100), (0,0,0), pygame.font.Font('freesansbold.ttf', 20))
btnPrevPage     = pygbutton.PygButton((10, 8, 100, 35), '<<', (100, 100, 100), (0,0,0), pygame.font.Font('freesansbold.ttf', 20))
btnNextPage     = pygbutton.PygButton((60 +  40 + 225, 8, 100, 35), '>>', (100, 100, 100), (0,0,0), pygame.font.Font('freesansbold.ttf', 20))
receiveButtons  = (btnGetMail, btnBack, btnPrevPage, btnNextPage)

btnReply        = pygbutton.PygButton((60 +  40 + 10, 8, 100, 35), 'Reply', (100, 100, 100), (0,0,0), pygame.font.Font('freesansbold.ttf', 20))
viewImageButtons = (btnBack, btnReply)

btnMessages     = {}

if not os.path.isfile('messages.json'):
    with open('messages.json', 'w') as outfile:
        json.dump([], outfile)

def MainMenu():
    for b in mainMenuButtons:
        b.draw(surface)
    if countUnread() > 0:
        imageNew = pygame.image.load("new.png")
        imageNew = imageNew.convert_alpha()
        surface.blit(imageNew, (width-85, 120))

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
    for b in receiveButtons:
        b.draw(surface)
    for b in btnMessages:
        btnMessages[b].draw(surface)
    pygame.draw.rect(surface, (30,30,30), (395-8,280-8,480,320))
    surface.blit(pygame.font.Font('freesansbold.ttf', 30).render(str(page+1) + "/" + str(totalPages() + 1), True, (200,200,200)), (395, 280))

def updateMailButtons():
    btns = {}
    imageNew = pygame.image.load("new.png")
    imageNew = imageNew.convert_alpha()
    for i, b in enumerate(jsonData):
        if i >= (page * 4) and i < ((page + 1) * 4):
            image = pygame.image.load(os.path.join('attachments', b['filename']))
            image = pygame.transform.scale(image, (225, 125))
            if b['read'] == 0:
                image.blit(imageNew, (225-75,0))
            btn = pygbutton.PygButton(((235 * ((i%4)%2)) + 10, (135 * ((i%4)/2)) + 50, 225, 125), '', (100, 100, 100), (0,0,0), pygame.font.Font('freesansbold.ttf', 20), image)
            btns[i] = btn
    return btns

def countUnread():
    count = 0
    for i in jsonData:
        if i['read'] == 0:
            count += 1
    return count

def getMail(dummy=None):
    global unreadMail, jsonData, btnMessages
    mailer.checkMail()
    with open('messages.json') as jsonFile:
        jsonData = json.load(jsonFile)
    print("Unread Mail: " + str(countUnread()))
    btnMessages = updateMailButtons()

def checkMail():
    global timerStarttime
    timerStarttime = time.time()
    thread.start_new_thread(getMail, (None, ))

def sendEmail():
    global view
    view = 1
    filename = str(int(time.time())) + ".png"
    if os.path.exists("./drawings") == False:
        os.mkdir("./drawings")
    pygame.image.save(drawCanvas, "./drawings/" + filename)
    thread.start_new_thread(mailer.sendImage, ("./drawings/", filename))
    drawCanvas.fill(canvasColor)

def ImageView():
    for b in viewImageButtons:
        b.draw(surface)
    if jsonData[image]['read'] == 0:
        jsonData[image]['read'] = 1
        btnMessages = updateMailButtons()
        writeJson()
    surface.blit(pygame.transform.scale(pygame.image.load("./attachments/" + jsonData[image]['filename']), (410, 260)), (35,50))

def writeJson():
    with open('messages.json', 'w') as outfile:
        json.dump(jsonData, outfile)

def totalPages():
    return int(math.floor((len(jsonData) - 1) / 4))

while 1:
    if time.time() > timerStarttime + (config.getint("Email", "interval")):
        timerStarttime = time.time()
        checkMail()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if pygame.key.get_focused() and pygame.key.get_pressed()[pygame.K_ESCAPE]:
            sys.exit()
        if view == 1: # Main Menu
            if 'click' in btnSend.handleEvent(event):
                view = 2  # Send
            if 'click' in btnRead.handleEvent(event):
                btnMessages = updateMailButtons()
                page = 0
                view = 3  # Read
            if 'click' in btnQuit.handleEvent(event):
                if config.getboolean('Env', 'debug'):
                    sys.exit()
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
            if 'click' in btnBack.handleEvent(event):
                view = 1
                drawCanvas.fill(canvasColor)
            if 'click' in btnSendDrawing.handleEvent(event):
                sendEmail()
        if view == 3: # Read
            if 'click' in btnGetMail.handleEvent(event):
                if time.time() > timerStarttime + 10:
                    checkMail()
            if 'click' in btnBack.handleEvent(event):
                view = 1
            if 'click' in btnPrevPage.handleEvent(event):
                if page > 0:
                    page -= 1
                    btnMessages = updateMailButtons()
            if 'click' in btnNextPage.handleEvent(event):
                if page < totalPages():
                    page += 1
                    btnMessages = updateMailButtons()
            for k in btnMessages:
                if 'click' in btnMessages[k].handleEvent(event):
                    image = k
                    view = 4
        if view == 4:
            if 'click' in btnBack.handleEvent(event):
                view = 3
                btnMessages = updateMailButtons()
            if 'click' in btnReply.handleEvent(event):
                view = 2
                btnMessages = updateMailButtons()
                drawCanvas.blit(pygame.transform.scale(pygame.image.load("./attachments/" + jsonData[image]['filename']), (410, 260)), (0,0))

    surface.fill((30,30,30))


    if view == 1:
        MainMenu()
    elif view == 2:
        SendMenu()
    elif view == 3:
        ReadMenu()
    elif view == 4:
        ImageView()
    else:
        view = 1

    pygame.display.flip()

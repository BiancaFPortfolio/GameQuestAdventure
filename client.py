import pygame
from network import Network
from ui import *
import threading

clientNum = 0

#UI elements
width = 1280
height = 720
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")
#Network object
net = Network()
#For logins/account creation
userField = InputField(100, 250, 200, 32, "Username")
passField = InputField(100, 300, 200, 32, "Password")
newButton = LoginButton(110, 360, 80, 32, "Create", "new")
returningButton = LoginButton(210, 360, 80, 32, "Login", "login")
#Animation counter
menuAnimation = 0
#Character positioning
START_X = 320
START_Y = 18
#Board 
b = None

def redrawWindow():
    win.fill((0, 0, 0))
    pygame.display.update()


def main():
    global b
    clock = pygame.time.Clock()

    running = True
    main_menu_running = True
    #Background
    backgroundAnimation = pygame.image.load("./Graphics/MenuSplashAnimation/pixil-frame-0.png")
    imagerect = backgroundAnimation.get_rect()
    win.blit(backgroundAnimation, imagerect)
    
    pygame.display.update()
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            try:
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                if main_menu_running:
                    x = threading.Thread(target = main_menu_draw, args = ())
                    x.start()
                    chara = main_menu(event)
                    x.join()
                    if chara != None:
                        chara.decode()
                        main_menu_running = False
                        create_board()
                else:
                    #Poll server for updated character information and monster stats
                    chara = net.send("character").decode()
                    chara = chara.split("=")
                    character_stats(chara[0])
                    monster_stats(chara[1])
                    #Update build of board on thread because costly
                    x = threading.Thread(target = update_board, args = (b, ))
                    x.start()
                    update_action(event)
                    x.join()
                    pygame.display.update()
            except Exception as e:
                print(e)

def main_menu(event):
    #User authentication UI
    #Send String to server in the form "username:password"
    #Password will then be converted to hash and the corresponding character will be returned and gameplay may commence
    userField.handle_event(event)
    passField.handle_event(event)
    #Will stop main_menu_running if user successfully logs in
    log = newButton.handle_event(event, userField.text, passField.text, net)
    if log == None:
        log = returningButton.handle_event(event, userField.text, passField.text, net)

    return log

def main_menu_draw():
    #global menuAnimation
    
    #if menuAnimation >= 0 and menuAnimation <= 15:
        #backgroundAnimation = pygame.image.load("./Graphics/MenuSplashAnimation/pixil-frame-{}.png".format(menuAnimation))
    #menuAnimation += 1
    userField.draw(win)
    passField.draw(win)
    newButton.draw(win)
    returningButton.draw(win)
    pygame.display.update()

def update_action(event):
    if event.type == pygame.KEYDOWN:
        #UPGRADE TO 3.10 FOR MATCHES
        #Directional
        if event.key == pygame.K_w:
            net.send("w")
        elif event.key == pygame.K_s:
            net.send("s")
        elif event.key == pygame.K_a:
            net.send("a")
        elif event.key == pygame.K_d:
            net.send("d")
        elif event.key == pygame.K_f:
            net.send("f")

def create_board():
    global b
    #Will constantly rebuild the board from the data in the server
    redrawWindow()
    try:
        boardState = net.send("board").decode()
        board = boardState.split("@")
        b = Board("", win, board)
        b.draw()
        pygame.display.update()
    except Exception as e:
        print(e)
    
def update_board(b):
    try:
        boardState = net.send("board").decode()
        board = boardState.split("@")
        b.update(board)
        pygame.display.update()
    except Exception as e:
        print(e)

def character_stats(character):
    chara = CharacterInterface(20, 20, 240, 680, character)
    chara.draw(win)
    pygame.display.update()
    

def monster_stats(monster):
    mon = MonsterInterface(1020, 20, 240, 680, monster)
    mon.draw(win)
    pygame.display.update()

if __name__ == "__main__":
    main()
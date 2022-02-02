import pygame
from network import Network
from ui import *
import threading

clientNum = 0

pygame.init()

#UI elements
width = 1280
height = 720
win = pygame.display.set_mode((width, height))
#win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
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
#Button dictionary to access in constant time
gameButtons = {pygame.K_w : "w", pygame.K_s : "s",
                pygame.K_a : "a", pygame.K_d : "d", 
                pygame.K_f : "f", pygame.K_1 : "1", 
                pygame.K_2 : "2", pygame.K_3 : "3", 
                pygame.K_4 : "4", pygame.K_5 : "5",
                pygame.K_6 : "6", pygame.K_7 : "7",
                pygame.K_8 : "8", pygame.K_9 : "9",
                pygame.K_0 : "0", pygame.K_u : "u",
                pygame.K_i : "i", pygame.K_o : "o", 
                pygame.K_p : "p"}

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
        clock.tick_busy_loop(60)

        for event in pygame.event.get():
            try:
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                if main_menu_running:
                    main_menu_draw()
                    chara = main_menu(event)
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
                    update_board(b)
                    update_action(event)
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
        #Use dictionary to send in constant time
        net.send(gameButtons.get(event.key))
        
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
    except Exception as e:
        print(e)

def character_stats(character):
    chara = CharacterInterface(20, 20, 240, 680, character)
    chara.draw(win)
    

def monster_stats(monster):
    mon = MonsterInterface(1020, 20, 240, 680, monster)
    mon.draw(win)

if __name__ == "__main__":
    main()
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

def redrawWindow():
    win.fill((255, 255, 255))
    pygame.display.update()


def main():
    clock = pygame.time.Clock()

    running = True
    main_menu_running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if main_menu_running:
                chara = main_menu(event)
                if chara != None:
                    main_menu_running = False
            else:
                x = threading.Thread(target = update_board, args = (0,))
                x.start()
                update_action(event, "")
                x.join()
                

def main_menu(event):
    #User authentication UI
    #Send String to server in the form "username:password"
    #Password will then be converted to hash and the corresponding character will be returned and gameplay may commence
    main_menu_draw()
    userField.handle_event(event)
    passField.handle_event(event)
    #Will stop main_menu_running if user successfully logs in
    log = newButton.handle_event(event, userField.text, passField.text, net)
    if log == None:
        log = returningButton.handle_event(event, userField.text, passField.text, net)
    main_menu_draw()

    return log

def main_menu_draw():
    global menuAnimation
    backgroundAnimation = pygame.image.load("./Graphics/MenuSplashAnimation/pixil-frame-0.png")
    if menuAnimation >= 0 and menuAnimation <= 15:
        backgroundAnimation = pygame.image.load("./Graphics/MenuSplashAnimation/pixil-frame-{}.png".format(menuAnimation))
    imagerect = backgroundAnimation.get_rect()
    win.blit(backgroundAnimation, imagerect)
    menuAnimation += 1
    userField.draw(win)
    passField.draw(win)
    newButton.draw(win)
    returningButton.draw(win)
    pygame.display.update()

def update_action(event, character):
    #Updates the character sprite and statistics based on the pygame events and sends updates to server
    if event.type == pygame.KEYDOWN:
        #UPGRADE TO 3.10 FOR MATCHES
        #Directional
        if event.key == pygame.KEY_W:
            pass
        elif event.key == pygame.KEY_S:
            pass
        elif event.key == pygame.KEY_A:
            pass
        elif event.key == pygame.KEY_D:
            pass

    pass

def update_board(threadID):
    #Will constantly rebuild the board from the data in the server
    boardState = net.send("board")
    boardState.split("@")
    b = Board("", win)
    b.draw()
    pygame.display.update()

if __name__ == "__main__":
    main()
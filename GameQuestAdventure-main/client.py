import pygame
from network import Network
from ui import *

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
                main_menu_running = main_menu(event)
            else:
                redrawWindow()

def main_menu(event):
    #User authentication UI
    #Send String to server in the form "username:password"
    #Password will then be converted to hash and the corresponding Player will be returned and gameplay may commence
    main_menu_draw()
    #INSTEAD OF HAVING TWO SETS OF FIELDS, JUST HAVE TWO BUTTONS AND NO ENTER EFFECT
    userField.handle_event(event)
    passField.handle_event(event)
    newButton.handle_event(event, userField.text, passField.text, net)
    returningButton.handle_event(event, userField.text, passField.text, net)
    main_menu_draw()

    return True

def main_menu_draw():
    win.fill((255, 255, 255))
    userField.draw(win)
    passField.draw(win)
    newButton.draw(win)
    returningButton.draw(win)
    pygame.display.update()

if __name__ == "__main__":
    main()
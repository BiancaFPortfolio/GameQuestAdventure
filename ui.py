import pygame
from network import Network
import json

pygame.init()
#UI constants
font = pygame.font.Font(None, 32)
inactive_color = pygame.Color(119, 136, 153) #LightSlateGray
active_color = pygame.Color(47, 79, 79) #DarkSlateGray
font_color = pygame.Color(0, 0, 0) #Black
active_font_color = pygame.Color(128, 128, 128)
BOX_PIXEL_GAP_XY = 8
TILE_XY = 32
start_X =320
start_Y = 18

class LoginButton:
    def __init__(self, x, y, w, h, text, ty):
        #Border
        self.outerRect = pygame.Rect(x, y, w, h)
        self.innerRect = pygame.Rect(x+4, y+4, w-4, h-4)
        self.text = text
        self.font = font
        self.font_color = font_color
        self.txt_surface = font.render(text, True, self.font_color)
        self.outerColor = active_color
        self.innerColor = inactive_color
        self.type = ty
    
    def handle_event(self, event, user, password, net):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.outerRect.collidepoint(event.pos):
                temp = self.outerColor 
                self.outerColor = self.innerColor
                self.innerColor = temp
                #Convert to string and send to server with indication of whether or not this is a new user
                sendString = user + "@" + password + "@" + self.type
                character = net.send(sendString)
                if character != None:
                    return False
        
        return True
        

    def draw(self, win):
        pygame.draw.rect(win, self.outerColor, self.outerRect)
        pygame.draw.rect(win, self.innerColor, self.innerRect)
        win.blit(self.txt_surface, (self.outerRect.x+BOX_PIXEL_GAP_XY, self.outerRect.y+BOX_PIXEL_GAP_XY))

        

class InputField:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.original_text = text
        self.font = font
        self.font_color = font_color
        self.txt_surface = font.render(text, True, self.font_color)
        self.color = inactive_color
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.font = active_font_color
                self.color = active_color
                if self.text == "Username" or self.text == "Password":
                    self.text = ""
            else:
                self.active = False
                self.font_color = font_color
                self.color = inactive_color
                
        elif event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                    self.color = inactive_color
                    self.text = ""
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pygame.K_AT:
                    #Cannot use @ symbol because that will separate values in TCP data
                    pass
                else:
                    if len(self.text) < 14:
                        self.text += event.unicode
        
        self.txt_surface = font.render(self.text, True, self.font_color)
        
    def draw(self, win):
        win.blit(self.txt_surface, (self.rect.x+BOX_PIXEL_GAP_XY, self.rect.y+BOX_PIXEL_GAP_XY))
        pygame.draw.rect(win, self.color, self.rect, 2)

class FreeText:
    def __init__(self, text):
        self.text = text
        self.font_color = font_color
        self.txt_surface = font.render(self.text, True, self.font_color)
        
    def draw(self, win, x, y):
        win.blit(self.txt_surface, (x, y))

class Board:
    def __init__(self, world, win):
        self.Tileset = []
        self.world = world
        self.win = win

    def draw(self):
        x = start_X
        y = start_Y
        #For tile, draw tile and monster on tile
        for i in range(0, 20):
            col = []
            for j in range(0, 20):
                #NEED TO CHANGE 0 ONCE UNITS ARE WORKED ON, pass string into init from server that has enemy and player data per tile
                t = Tile(x, y, self.world, 0)
                col.append(t)
                t.draw(win)
                x += TILE_XY
            self.Tileset.append(col)
            y += TILE_XY
            x = start_X
        
        #Print shop
        t = Tile(start_X, 720-92, "shop", 0)
        self.Tileset[0][19]
        t.draw(win)

class Tile:
    def __init__(self, x, y, world, unit):
        self.rect = pygame.Rect(x, y, TILE_XY, TILE_XY)
        if world == "shop":
            self.image = pygame.image.load("./Graphics/Sprites/shop.png")
        else:
            self.image = pygame.image.load("./Graphics/Sprites/CandyTile.png")
        #USE TO PICK TILESET TO PRINT LATER
        self.world = world
        self.unit = unit
        pass

    def draw(self, win):
        win.blit(self.image, self.rect)

    def unitFill(self, unit):
        pass

#Testing suite for game board
#clock = pygame.time.Clock()
#while True:
#    clock.tick(60)
#    win = pygame.display.set_mode((1280, 720))     
#    b = Board(0, win)
#    b.draw()
#    pygame.display.update()
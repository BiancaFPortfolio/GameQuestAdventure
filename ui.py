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
BOX_PIXEL_GAP_X = 8
BOX_PIXEL_GAP_Y = 8

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
                print(character)
        

    def draw(self, win):
        pygame.draw.rect(win, self.outerColor, self.outerRect)
        pygame.draw.rect(win, self.innerColor, self.innerRect)
        win.blit(self.txt_surface, (self.outerRect.x+BOX_PIXEL_GAP_X, self.outerRect.y+BOX_PIXEL_GAP_Y))

        

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
        win.blit(self.txt_surface, (self.rect.x+BOX_PIXEL_GAP_X, self.rect.y+BOX_PIXEL_GAP_Y))
        pygame.draw.rect(win, self.color, self.rect, 2)

class FreeText:
    def __init__(self, text):
        self.text = text
        self.font_color = font_color
        self.txt_surface = font.render(self.text, True, self.font_color)
        
    def draw(self, win, x, y):
        win.blit(self.txt_surface, (x, y))

class Board:
    def __init__(self, id, world):
        self.Tileset = []
        for i in 100:
            self.Tileset[i] = Tile(i, )

    def draw(self):
        #For tile, draw tile and monster on tile
        pass

class Tile:
    def __init__(self, id, TileSprite):
        pass

    def draw(self):
        pass

    def unitFill(self, unit):
        pass

                    

import pygame
from network import Network

pygame.init()
#UI constants
font = pygame.font.Font(None, 32)
small_font = pygame.font.Font(None, 16)
inactive_color = pygame.Color(119, 136, 153) #LightSlateGray
active_color = pygame.Color(47, 79, 79) #DarkSlateGray
font_color = pygame.Color(0, 0, 0) #Black
active_font_color = pygame.Color(128, 128, 128)
BOX_PIXEL_GAP_XY = 8
TILE_XY = 32
start_X = 320
start_Y = 18

class MonsterInterface:
    def __init__(self, x, y, w, h, monster):
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.bg_color = active_color
        self.font_color = pygame.Color(255, 255, 255)
        try:
            self.mon = monster.split(":")
            self.name = self.mon[1]
            self.lootLevel = "Loot level: " + self.mon[2]
            self.difficultyClass = "DC: +" + self.mon[3]
            self.hp = "HP: " + self.mon[4]
        except:
            self.mon = ""
            self.name = ""
            self.lootLevel = ""
            self.difficultyClass = ""
            self.hp = ""

        #Text
        self.nameText = font.render(self.name, True, self.font_color)
        self.HPText = font.render(self.hp, True, self.font_color)
        self.dcText = font.render(self.difficultyClass, True, self.font_color)
        self.lootText = font.render(self.lootLevel, True, self.font_color)

    def draw(self, win):
        pygame.draw.rect(win, self.bg_color, self.rect)
        if self.mon != "":
            win.blit(self.nameText, (self.rect.x+BOX_PIXEL_GAP_XY, self.rect.y+20))
            win.blit(self.HPText, (self.rect.x+BOX_PIXEL_GAP_XY, self.rect.y+50))
            win.blit(self.dcText, (self.rect.x+BOX_PIXEL_GAP_XY, self.rect.y+80))
            win.blit(self.lootText, (self.rect.x+BOX_PIXEL_GAP_XY, self.rect.y+110))


class CharacterInterface:
    def __init__(self, x, y, w, h, character):
        self.rect = pygame.Rect(x, y, w, h)
        self.character = character.split("@")
        self.bgcolor = active_color
        self.font_color = pygame.Color(255, 255, 255)
        #Character name
        self.name = self.character[0]
        #Health
        self.health = "HP: " + self.character[1]
        #Arnor bonus
        self.armorBonus = "Armor: +" + self.character[2]
        #Weapon bonus
        self.weaponBonus = "Weapon: +" + self.character[3]
        #Gold and inventory assignments
        self.gold = self.character[4] + " gold"
        self.inventory = []
        armorFlag = False
        itemFlag = False
        for i in self.character[6:]:
            if i == "armor":
                armorFlag = True
            elif i == "items":
                itemFlag = True
            else:
                #Build inventory item string
                spl = i.split(":")
                if not armorFlag:
                    splStr = spl[0] + " : Weapon +" + str(spl[1]) #+ " : " + str(spl[2]) + "g"
                elif not itemFlag:
                    splStr = spl[0] + " : Armor +" + str(spl[1]) #+ " : " + str(spl[2]) + "g"
                else:
                    splStr = spl[0] + " : Armor +" + str(spl[1]) #+ " : " + str(spl[2]) + "g"
                
                self.inventory.append(splStr)
        #Text
        self.nameText = font.render(self.name, True, self.font_color)
        self.HPText = font.render(self.health, True, self.font_color)
        self.ArmorText = font.render(self.armorBonus, True, self.font_color)
        self.WeaponText = font.render(self.weaponBonus, True, self.font_color)
        self.goldText = font.render(self.gold, True, self.font_color)

    def draw(self, win):
        pygame.draw.rect(win, self.bgcolor, self.rect)
        win.blit(self.nameText, (self.rect.x+BOX_PIXEL_GAP_XY, self.rect.y+20))
        win.blit(self.HPText, (self.rect.x+BOX_PIXEL_GAP_XY, self.rect.y+50))
        win.blit(self.ArmorText, (self.rect.x+BOX_PIXEL_GAP_XY, self.rect.y+80))
        win.blit(self.WeaponText, (self.rect.x+BOX_PIXEL_GAP_XY, self.rect.y+110))
        win.blit(self.goldText, (self.rect.x+BOX_PIXEL_GAP_XY, self.rect.y+140))
        self.drawInventory(win)

    def drawInventory(self, win):
        #Loop through inventory and blit the text in little bars, 
        #In server, create an inventory max to avoid graphical bugs
        y = 240
        for i in range(0, 10):
            #Print 10 inventory boxes
            rect = pygame.Rect(self.rect.x, y, 240, 30)
            pygame.draw.rect(win, inactive_color, rect)
            y += 35
            #Check if i matches to an inventory index to fill the slot
            try:
                #Render text
                text = small_font.render(self.inventory[i], True, self.font_color)
                #Blit text
                win.blit(text, (rect.x+BOX_PIXEL_GAP_XY, rect.y+10))
            except:
                #Not a valid index, do nothing
                pass

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
                return character
        
        return None
        

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
    def __init__(self, world, win, boardData):
        self.boardData = boardData
        self.Tileset = []
        self.world = world
        self.win = win

    def draw(self):
        x = start_X
        y = start_Y
        #Counter for boardData
        k = 0
        #For tile, draw tile and monster on tile
        for i in range(0, 20):
            col = []
            for j in range(0, 20):
                #NEED TO CHANGE 0 ONCE UNITS ARE WORKED ON, pass string into init from server that has enemy and player data per tile
                t = Tile(x, y, self.world, self.boardData[k])
                col.append(t)
                t.draw(self.win)
                x += TILE_XY
                k+=1
            self.Tileset.append(col)
            y += TILE_XY
            x = start_X
        
        #Print shop
        t = Tile(start_X, 720-92, "shop", "0")
        self.Tileset[19][0] = t
        t.draw(self.win)

    def update(self, boardData):
        #Function to just draw the monster and player updates without redrawing the whole board
        #Will naively do this simply by drawing only the monsters and players with this function,
        #But will revisit, performance depending, and consider adding a marker for entities changing states
        self.boardData = boardData
        k = 0

        for i in range(0, 20):
            for j in range(0, 20):
                if self.boardData[k] != "0":
                    self.Tileset[i][j].unitFill(self.win, self.boardData[k])
                else:
                    self.Tileset[i][j].unitErase(self.win)
                k += 1
        #Shop
        t = Tile(start_X, 720-92, "shop", "0")
        self.Tileset[19][0] = t
        t.draw(self.win)

class Tile:
    def __init__(self, x, y, world, unit):
        self.rect = pygame.Rect(x, y, TILE_XY, TILE_XY)
        self.world = world
        #String representation of enemy/player
        self.unit = unit
        #Object representation of enemy/player
        self.entity = None
        if self.world == "shop":
            self.image = pygame.image.load("./Graphics/Sprites/shop.png")
        #Will need changed to elifs for other sprites OR UPGRADE TO PYTHON 3.10 FOR MATCHES
        else:
            self.image = pygame.image.load("./Graphics/Sprites/CandyTile.png")
        #USE TO PICK TILESET TO PRINT LATER
        

    def draw(self, win):
        win.blit(self.image, self.rect)
        #Append if statement for if unit != 0, unitFill
        if self.unit != "0":
            self.unitFill(win, self.unit)

    def unitFill(self, win, unit):
        #Fills a tile with a Monster or Player and draws the Monster/Player
        self.unit = unit
        self.entity = self.Entity(self.rect, self.unit)
        self.entity.draw(win)

    def unitErase(self, win):
        if self.unit != "0":
            self.unit = "0"
            self.entity = None
            self.draw(win)

    class Entity:
        #Takes unit and converts it to a printable Monster/Player on top of the Tile
        def __init__(self, rect, unit):
            self.rect = rect
            self.unit = unit
            self.image = None
            #ANOTHER GOOD AREA FOR MATCH CASE AFTER YOU UPDATE TO 3.10
            #ALSO ONCE MORE ENEMY DETAILS ARE MADE, STRING WILL BE SPLIT WITH : FOR UNIT STATS
            if self.unit == "1":
                #Client Player
                self.image = pygame.image.load("./Graphics/Sprites/Player.png")
            elif self.unit == "2":
                #Other Player
                self.image = pygame.image.load("./Graphics/Sprites/OtherPlayer.png")
            else:
                #Green Slime
                self.image = pygame.image.load("./Graphics/Sprites/GreenSlime.png")

        def draw(self, win):
            win.blit(self.image, self.rect)

#Testing suite for game board
#clock = pygame.time.Clock()
#while True:
#    clock.tick(60)
#    win = pygame.display.set_mode((1280, 720))     
#    b = Board(0, win)
#    b.draw()
#    pygame.display.update()
import random
from character import *
#Game information
worlds = ["Green Vale", "Shelly Shore", "The Spire", "Toadstool Bog", "Tiptop Mountain", "Candy Castle"]
shops = ["Tom's", "The Fish Market", "Rocky Road Supplies", "Swampy Place", "Snow Is Us", "Candy Shop"]
#Combat
#Decided by dice roll. If dice roll higher than difficulty class, monster dies or takes damage
#If dice roll is lower than difficulty class, player takes damage
#Equipment
#Armor adds health to player
#Weapon adds modifier to dice roll
#Dice
#2d10 are rolled every combat turn

class World:
    def __init__(self, id, name, level):
        self.id = id
        self.monsterList = []
        self.name = name
        self.level = level
        #0 is empty tile
        self.map = [[0 for i in range(21)] for j in range(21)]
        self.monsterCount = 0
        self.monsterCap = 20

    def addMonster(self):
        #Roll for random tile until find empty tile
        while self.monsterCount < self.monsterCap:
            rollIf = random.randint(0, 150)
            #If greater than 10, break. No spawn
            if rollIf > 1:
                break
            else:
                rollX = random.randint(2, 18)
                rollY = random.randint(2, 18)
                if self.map[rollX][rollY] == 0:
                    #Roll for random monster from world's monster list
                    #FOR NOW ONLY ONE MONSTER SO JUST 3
                    #ALSO CHANGE TO INCLUDE STATS LATER
                    self.map[rollX][rollY] = Monster(3, "Green Slime", 1, 2, 2)
                    self.monsterCount += 1
                    break

    def addPlayer(self, character):
        #Player will always spawn at 0, 0 on the first world when they login. Map is small, so this is a nonissue
        if self.map[0][0] == 0:
            self.map[0][0] = []
        self.map[0][0].append(character)

    def movePlayer(self, character, x, y, prevX, prevY):
        oldTile = self.map[prevX][prevY]
        for i in oldTile:
            if character.__eq__(i):
                oldTile.remove(character)
            #Empty lists are False in python
            if not oldTile:
                self.map[prevX][prevY] = 0
                
        if self.map[x][y] == 0:
            self.map[x][y] = []
        self.map[x][y].append(character)

    def __toString__(self, character):
        #Server will now pass in character, this will match on every character token in the map and add 1 to the string instead of 2 if the character matches this one
        s = ""
        for i in range(0, 20):
            for j in range(0, 20):
                if self.map[i][j] == 0:
                    s += "0"
                elif isinstance(self.map[i][j], Monster):
                    s += self.map[i][j].__toString__()
                elif isinstance(self.map[i][j], list):
                    isChara = False
                    for k in self.map[i][j]:
                        if character.__eq__(k):
                            isChara = True
                    if isChara:
                        s += "1"
                    else:
                        s += "2"

                if i != 20 and j != 20:
                    s += "@"
        
        return s

class Monster:
    def __init__(self, id, name, lootLevel, difficultyClass, hp):
        self.id = id
        self.name = name
        self.lootLevel = lootLevel
        self.difficultyClass = difficultyClass
        self.hp = hp

    def __toString__(self):
        string = str(self.id) + ":" + self.name + str(self.lootLevel) + ":" + str(self.difficultyClass) + ":" + str(self.hp)
        return string

class Shop:
    def __init__(self, id, itemList):
        self.id = id
        self.itemList = itemList

class NPC:
    def __init__(self):
        pass

class Loot:
    def __init__(self):
        pass

class Game:
    def __init__(self):
        #Initialize 6 worlds
        self.worldList = []
        for x in worlds:
            w = World(x, worlds[x], x+1)
            self.worldList.append()
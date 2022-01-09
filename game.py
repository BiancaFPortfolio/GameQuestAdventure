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
        self.map = [20*[0]]*20

    def addMonster(self):
        #Roll for random tile until find empty tile
        #Roll for random monster from world's monster list
        #self.map[i][j] = monster id
        #As client builds map, Tiles will plug in monster id and get appropriate sprite
        #0 = empty tile, 1 = client player, 2 = other player, so 3 and greater are valid monster ids
        pass

    def __toString__(self):
        s = ""
        for i in range(0, 20):
            for j in range(0, 20):
                s += str(self.map[i][j])
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
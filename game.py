#Game information
worlds = ["Green Vale", "Shelly Shore", "The Spire", "Toadstool Bog", "Tiptop Mountain", "Candy Castle"]
hubs = ["Tom's", "The Fish Market", "Rocky Road Supplies", "Swampy Place", "Snow Is Us", "Candy Shop"]
#Combat
#Decided by dice roll. If dice roll higher than difficulty class, monster dies or takes damage
#If dice roll is lower than difficulty class, player takes damage
#Equipment
#Armor adds health to player
#Weapon adds modifier to dice roll
#Dice
#2d10 are rolled every combat turn


class World:
    def __init__(self, id, name, level, hub):
        self.id = id
        self.monsterList = []
        self.name = name
        self.level = level
        self.hub = Hub(self.id, hub)

class Monster:
    def __init__(self, id, name, lootLevel, difficultyClass, hp):
        self.id = id
        self.name = name
        self.lootLevel = lootLevel
        self.difficultyClass = difficultyClass
        self.hp = hp

class Hub:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class Shop:
    def __init__(self, id, name, owner, itemList):
        self.id = id
        self.name = name
        self.owner = owner
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
            w = World(x, worlds[x], x+1, hubs[x])
            self.worldList.append()
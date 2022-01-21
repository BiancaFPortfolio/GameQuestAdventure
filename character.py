import random

class Character:
    def __init__(self, name):
        self.name = name
        self.health = 3
        #Attacks will automatically occur with best in slot
        self.armor = {}
        self.weapons = {}
        self.armorStat = 0
        self.weaponStat = 0

    def getArmorStat(self):
        for k, v in self.armor:
            if int(v) > self.armorStat:
                self.armorStat = int(v)
        
        return self.armorStat
    
    def getWeaponStat(self):
        for i, v in self.weapons:
            if int(v) > self.weaponStat:
                self.weaponStat = int(v)

        return self.weaponStat

    def __eq__(self, chara):
        #Names are unique, can use to quickly compare
        if chara.name == self.name:
            return True
        return False

    def __toString__(self):
        string = self.name + "@" + str(self.health) + "@" + str(self.getArmorStat()) + "@" + str(self.getWeaponStat()) + "@weapons" 
        for k, v in self.weapons.items():
            string = string + "@" + k + ":" + v
        
        string += "@armor"

        for k, v in self.armor.items():
            string = string + "@" +  k + ":" + v

        return string

    def fromString(self, string):
        chara = string.split("@")
        self.name = chara[0]
        self.health = int(chara[1])
        armorFlag = False
        for i in chara[5:]:
            if i == "armor":
                armorFlag = True
            elif not armorFlag:
                item = i.split(":")
                self.weapons[item[0]] = item[1]
            elif armorFlag:
                item = i.split(":")
                self.armor[item[0]] = item[1]

    def roll(self):
        return random.randint(0, 20) + self.getWeaponStat()

#Testing suite for Character
#c = Character("")
#s = "Bumbles@5@weapons@The Icepick:1@armor@Leather Armor:1"
#c.fromString(s)
#print(c.__toString__())
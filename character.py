class Character:
    def __init__(self, name):
        self.name = name
        self.health = 5
        #Attacks will automatically occur with best in slot
        self.armor = {}
        self.weapons = {}
        self.armorStat = 0
        self.weaponStat = 0

    def getArmorStat(self):
        for k, v in self.armor:
            if v > self.armorStat:
                self.armorStat = v
        
        return self.armorStat
    
    def getWeaponStat(self):
        for i, v in self.weapons:
            if v > self.weaponStat:
                weaponStat = v

        return self.weaponStat

    def __toString_(self):
        string = self.name + "@" + self.health + "@weapons@"
        for k, v in self.armor:
            string = string + k + ":" + v + "@"
        
        string += "@armor@"

        for k, v in self.weapons:
            string = string + k + ":" + v + "@"

    def fromString(self, string):
        chara = string.split("@")
        self.name = chara[0]
        self.self.health = chara[1]
        i = 3
        for i in chara:
            if i != "armor":
                item = i.split(":")
                self.weapons[item[0]] = item[1]
            else: break
        
        for i in chara:
            item = i.split(":")
            self.armor[item[0]] = item[1]
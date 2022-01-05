class Character:
    def __init__(self, name):
        self.name = name
        self.health = 5
        #Attacks will automatically occur with best in slot
        self.armor = []
        self.weapons = []
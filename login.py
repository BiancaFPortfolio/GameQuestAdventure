#Hash table for login info
#Character data will be stored as .txt on server and upon login, sent to player. 
#This will prevent players from hacking in items
class Login:
    def __init__(self):
        #Dictionary to store key:value pairs of username:[password, character sheet]
        #Should eventually be initialized from file
        self.dict = {}

    def login(self, username, password):
        #Accepts raw username and password player submits and converts password to hash
        #Check for accurate login, do not disclose to player which information is incorrect
        #Returns either character sheet or None
        for k, v in self.dict.items():
            if username == k:
                hashedPass = self.__hash__(password)
                #Password
                if hashedPass == v[0]:
                    return v[1]
                else:
                    return None

    def create(self, username, password):
        #Accepts raw username and password from player, converts password to hash, stores as k:v pair
        #Error check for whether or not username is unique to the server
        #OLD KEYS ARE OVERWRITTEN BY DUPLICATE BY DEFAUALT IN PYTHON
        #Returns None if username exists in dict, else returns character sheet
        for k, v in self.dict.items():
            if username == k:
                return None
        #Replace with character sheet in string format
        character = "New character"
        self.dict[username] = [self.__hash__(password), character]
        return character

    def __hash__(self, value):
        #Returns hash
        return hash(value)

#Testing suite for login.py
#log = Login()
#print(log.dict.items())
#log.create("Kevin", ["dog123", "character"])
#print(log.dict.items())
#print(log.login("Kevin", "dog123"))
#print(log.login("Kev", "dog123"))
#print(log.login("Kevin", "dog1234"))
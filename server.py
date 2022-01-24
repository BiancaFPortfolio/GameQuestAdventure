from _thread import *
from re import X
import socket
import pygame
from game import *
from login import Login

#Server globals
server = "10.0.2.15"
port = 5555
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER_CAP = 20
RECV_BITS = 2048
#Login hashmap
loginVerification = Login()
#BASE COMBAT STATS
BASE_DC = 10

try: 
    sock.bind((server, port))
except socket.error as e:
    str(e)

sock.listen(SERVER_CAP)
print("Server started.")

#Testing world
w = World(0, "Candy Castle", 1)

def log(conn):
    conn.send(str.encode("Connected to server."))
    reply = ""
    while True:
        try:
            data = conn.recv(RECV_BITS).decode("utf-8")

            if not data:
                pass
            else:
                #String split data
                loginData = data.split("@", 3)
                try:
                    if(loginData[2] == "new"):
                        character = loginVerification.create(loginData[0], loginData[1])
                        conn.send(str.encode(character))
                        print(character)
                        if character != None:
                            play(conn, character)
                    elif(loginData[2] == "login"):
                        character = loginVerification.login(loginData[0], loginData[1])
                        conn.send(str.encode(character))
                        if character != None:
                            play(conn, character)
                except:
                    #Send string indicating login failure
                    pass
        except Exception as e:
            print(e)
            break
    
    print("Player has lost connection.")
    conn.close()
        
def play(conn, character):
    w.addPlayer(character)
    x = 0
    y = 0
    monsterTarget = None
    mon = ""
    characterSheet = Character("")
    characterSheet.fromString(character)
    targetX = 0
    targetY = 0
    while True:
        try:
            #Check for poll from client
            data = conn.recv(RECV_BITS).decode("utf-8")
            
            if not data:
                pass
            else:
                if data == "board":
                    #Send game board data to player over conn
                    conn.send(str.encode(w.__toString__(character)))
                elif data == "character":
                    #Targeting variables
                    mon = ""
                    monsterTarget = None
                    targetX = 0
                    targetY = 0
                    #Will go clockwise from y+1 to x-1
                    if isinstance(w.map[x][y+1], Monster):
                        mon = w.map[x][y+1].__toString__()
                        monsterTarget = w.map[x][y+1]
                        targetX = x
                        targetY = y+1
                    elif isinstance(w.map[x+1][y], Monster):
                        mon = w.map[x+1][y].__toString__()
                        monsterTarget = w.map[x+1][y]
                        targetX = x+1
                        targetY = y
                    elif isinstance(w.map[x][y-1], Monster):
                        mon = w.map[x][y-1].__toString__()
                        monsterTarget = w.map[x][y-1]
                        targetX = x
                        targetY = y-1
                    elif isinstance(w.map[x-1][y], Monster):
                        mon = w.map[x-1][y].__toString__()
                        monsterTarget = w.map[x-1][y]
                        targetX = x-1
                        targetY = y
                    conn.send(str.encode(character + "=" + mon))
                elif data == "f":
                    #Combat
                    #Verify that a Monster exists to attack
                    if monsterTarget != None:
                        #Establish dice threshold that player's roll has to surpass for a successful attack
                        dc = BASE_DC + int(monsterTarget.difficultyClass)
                        #Take Character object from map
                        for i in w.map[x][y]:
                            ch = Character("")
                            ch.fromString(i)
                            if ch.__eq__(characterSheet):
                                roll = ch.roll()
                                #Roll with roll function on Character
                                if roll >= dc:
                                    monsterTarget.hp -= 1
                                    if monsterTarget.hp == 0:
                                        #remove from map
                                        w.map[targetX][targetY] = 0
                                        w.monsterCount -= 1
                                        #HAVE PLAYER ROLL ON LOOT TABLE AND RECEIVE GOLD OR ITEMS
                                        lootTable(monsterTarget, ch)
                                        #Update character
                                        w.map[x][y].remove(i)
                                        character = ch.__toString__()
                                        w.map[x][y].append(character)
                                else:
                                    #Deduct health from Character
                                    ch.health -= 1
                                    w.map[x][y].remove(i)
                                    if ch.health == 0:
                                        #Reset previous tile character was on
                                        if not w.map[x][y]:
                                            w.map[x][y] = 0
                                        ch.health = ch.getArmorStat()+3
                                        character = ch.__toString__()
                                        w.movePlayer(character, 0, 0, x, y)
                                        x = 0
                                        y = 0
                                        characterSheet = ch
                                    else:
                                        character = ch.__toString__()
                                        w.map[x][y].append(character)
                    conn.send(str.encode(w.__toString__(character)))
                else:
                    #Data will be command from Player
                    if data == "d" and y < 19:
                        if w.map[x][y+1] == 0 or isinstance(w.map[x][y+1], list):
                            w.movePlayer(character, x, y+1, x, y)
                            y += 1
                    elif data == "a" and y > 0:
                        if w.map[x][y-1] == 0 or isinstance(w.map[x][y-1], list):
                            w.movePlayer(character, x, y-1, x, y)
                            y -= 1
                    elif data == "w" and x > 0:
                        if w.map[x-1][y] == 0 or isinstance(w.map[x-1][y], list):
                            w.movePlayer(character, x-1, y, x, y)
                            x -= 1
                    elif data == "s" and x < 19:
                        if w.map[x+1][y] == 0 or isinstance(w.map[x+1][y], list):
                            w.movePlayer(character, x+1, y, x, y)
                            x += 1
                        pass
                    conn.send(str.encode(w.__toString__(character)))
            #Update board
            w.addMonster()
        except Exception as e:
            print(e)
            break
    
    print("Player has lost connection.")
    conn.close()

def lootTable(monster, character):
    table = monster.lootLevel
    roll = random.randint(0, 99)
    if table == 1:
        if roll < 30:
            character.gold += 1
        elif roll < 60:
            character.gold += 2
        elif roll < 80:
            character.gold += 3
        elif roll < 90:
            #Rare weapon drop
            character.weapons["Scythe of a Poor Soul"] = 1
            character.weaponStat = 1
        else:
            #Rare armor drop
            character.armor["Slimy sleeves"] = 1
            character.armorStat = 1
    else:
        pass

while True:
    conn, addr = sock.accept()
    print("Player entering: ", addr)

    start_new_thread(log, (conn,))
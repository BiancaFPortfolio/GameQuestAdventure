from _thread import *
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
                    mon = ""
                    monsterTarget = None
                    #Will go clockwise from y+1 to x-1
                    if isinstance(w.map[x][y+1], Monster):
                        mon = w.map[x][y+1].__toString__()
                        monsterTarget = w.map[x][y+1]
                    elif isinstance(w.map[x+1][y], Monster):
                        mon = w.map[x+1][y].__toString__()
                        monsterTarget = w.map[x+1][y]
                    elif isinstance(w.map[x][y-1], Monster):
                        mon = w.map[x][y-1].__toString__()
                        monsterTarget = w.map[x][y-1]
                    elif isinstance(w.map[x-1][y], Monster):
                        mon = w.map[x-1][y].__toString__()
                        monsterTarget = w.map[x-1][y]
                    conn.send(str.encode(character + "=" + mon))
                elif data == "f":
                    #Combat
                    #Verify that a Monster exists to attack
                    if monsterTarget != None:
                        #Establish dice threshold that player's roll has to surpass for a successful attack
                        dc = BASE_DC + int(monsterTarget.difficultyClass)
                        #Take Character object from map
                        for i in w.map[x][y]:
                            if i.__eq__(characterSheet):
                                roll = i.roll()
                                #Roll with roll function on Character
                                if roll >= dc:
                                    monsterTarget.hp -= 1
                                    if monsterTarget.hp == 0:
                                        #remove from map
                                        pass
                                else:
                                    #Deduct health from Character
                                    i.health -= 1
                                    if i.health == 0:
                                        i.health = i.getArmorStat()+3
                                        w.movePlayer(i, 0, 0, x, y)
                                        x = 0
                                        y = 0
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
                print(w.__toString__(character))
            #Update board
            w.addMonster()
        except Exception as e:
            print(e)
            break
    
    print("Player has lost connection.")
    conn.close()


while True:
    conn, addr = sock.accept()
    print("Player entering: ", addr)

    start_new_thread(log, (conn,))
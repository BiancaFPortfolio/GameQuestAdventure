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
    while True:
        try:
            #Check for poll from client
            data = conn.recv(RECV_BITS).decode("utf-8")
            
            if not data:
                pass
            else:
                if data == "board":
                    #Send game board data to player over conn
                    conn.send(str.encode(w.__toString__()))
                else:
                    #Data will be command from Player
                    pass
            #Read player action
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
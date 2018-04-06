# Python program to implement server side of chat room.
import socket
import commands
import select
import sys
from _thread import *
 
"""The first argument AF_INET is the address domain of the
socket. This is used when we have an Internet Domain with
any two hosts The second argument is the type of socket.
SOCK_STREAM means that data or characters are read in
a continuous flow."""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
 
# checks whether sufficient arguments have been provided
if len(sys.argv) != 3:
    print("Correct usage: script, IP address, port number")
    exit()
 
# takes the first argument from command prompt as IP address
IP_address = str(sys.argv[1])
 
# takes second argument from command prompt as port number
Port = int(sys.argv[2])
 
"""
binds the server to an entered IP address and at the
specified port number.
The client must be aware of these parameters
"""
server.bind((IP_address, Port))
 
"""
listens for 100 active connections. This number can be
increased as per convenience.
"""
server.listen(100)
 
list_of_clients = {}

#mining pool variables
mining_pool = {}
reward = 1
z1 = -1
z2 = -1
found = False
 
def clientthread(conn, addr):
 
    # sends a message to the client whose user object is conn
 
    while True:
            try:
                message = conn.recv(2048).decode("utf-8")
                if message:
                    
                    #if connection who sent message is the master, process their input
                    if list_of_clients[conn] == "master":
                        broadcast(message)
                        
                        #print("ja, dit is de master")
                        if message.startswith(commands.START_MINPOOL):
                            #master started the mining pool
                            print("yeaah, master started the mining pool")
                            z = message[len(commands.START_MINPOOL):].split()
                            z1 = int(z[0])
                            z2 = int(z[1])
                            
                            print("z1:" + str(z1))
                            print("z2:" + str(z2))
                    else:        
                        #client sends his/her name
                        if message.startswith(commands.HELLO):
                            name = message[len(commands.HELLO):].strip()
                            
                            if name not in list_of_clients.values():
                                list_of_clients[conn] = name
                                print(addr[0] + " picked the following name: " + name)
                            else:
                                conn.send((commands.ERROR_NAME).encode())
                        elif message.startswith(commands.SEND_MINPOOL):
                            #client sent a solution for the mining pool
                            name = list_of_clients[conn] + " (" + addr[0] + ")"
                            h = message[len(commands.SEND_MINPOOL):].strip(commands.DELIM)
                            
                            print(name + " found hash " + h)
                            print(found)
                            
                            #check if hash h starts with z1 or z2 zeros
                            if h.startswith("".join(["0"]*4)):
                                found = True
                                print("Yay. A hash starting with " + z1 + " zeros has been found by " + name)
                                
                                #split reward according to the amount of hashes all clients sent
                                #TODO
                                print("List of rewards:")
                                
                                for client in mining_pool:
                                    print(list_of_clients[client] + ": " + mining_pool[client] + ": " + mining_pool[client]*reward)
                            elif h.startswith("".join(["0"]*3)):
                                #increment client's amount for every time they send in valid hashes.
                                
                                conn.send((commands.CONT_MINPOOL).encode())
                                
                                if not mining_pool.has_key(conn):
                                    mining_pool[conn] = 1
                                else:
                                    mining_pool[conn] += 1
                            else:
                                print("er gaat volgens mij iets mis, hash start niet met z1 of z2 zeros")
                        else:
                            """prints the message and address of the
                            user who just sent the message on the server
                            terminal"""
                            print(name + " (" + addr[0] + "): " + message)
                else:
                    """message may have no content if the connection
                    is broken, in this case we remove the connection"""
                    remove(conn)
 
            except:
                continue
 
#broadcast message from server to all clients except the master
def broadcast(message):
    for client in list_of_clients:
        if list_of_clients[client] != "master":
            try:
                client.send(message.encode())
            except:
                client.close()
 
                # if the link is broken, we remove the client
                remove(client)

"""The following function simply removes the object
from the list that was created at the beginning of 
the program"""
def remove(conn):
    if conn in list_of_clients:
        del list_of_clients[conn]
 
while True:
    """Accepts a connection request and stores two parameters, 
    conn which is a socket object for that user, and addr 
    which contains the IP address of the client that just 
    connected"""
    conn, addr = server.accept()
 
    """Maintains a list of clients for ease of broadcasting
    a message to all available people in the chatroom"""
    list_of_clients[conn] = ""
 
    # prints the address of the user that just connected
    print(addr[0] + " connected")
 
    # creates and individual thread for every user 
    # that connects
    start_new_thread(clientthread,(conn,addr))
 
conn.close()
server.close()

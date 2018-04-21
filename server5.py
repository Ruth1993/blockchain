#server
import socket
import select
import sys
from _thread import *
import time
import commands
 
#setup server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
 
#checks if enough input arguments have been given
if len(sys.argv) != 3:
    print("Correct usage: server.py, <ip address>, <port number>")
    exit()

ip = str(sys.argv[1])
port = int(sys.argv[2])

#bind server to ip and port which have been extracted from the command line
server.bind((ip, port))

#at most 100 clients can connect to the server
server.listen(100)

#maintain list of clients with their connection as key and name as value
list_of_clients = {}

#proof of work variables
winner = None
counter = 0

#mining pool variables
mining_pool = {}
reward = 12.5
z1 = -1
z2 = -1
found = False
start = 0
 
def clientthread(conn, addr):
    global list_of_clients
        
    global winner
    global counter
    
    global mining_pool
    global z1
    global z2
    global found
    global reward
    global start
 
    while True:
            try:
                message = conn.recv(2048).decode("utf-8")
                
                if message:
                    
                    #if connection who sent message is the master, process their input
                    if list_of_clients[conn] == "master":
                        #always broadcast message from master to the clients/miners
                        broadcast(message)
                        
                        if message.startswith(commands.START_POW):
                            #master started proof of work, create a nice title
                            #first reset the winner
                            reset_pow()
                            
                            print_title("PROOF OF WORK")
                        elif message.startswith(commands.START_MINPOOL):
                            #master started the mining pool
                            
                            #first reset all variables in case they have already been set due to an earlier mining pool
                            reset_minpool()
                            
                            #start time needed for the mining pool
                            start = time.time()
                    
                            #print a nice title
                            print_title("MINING POOL")
                            
                            z = message[len(commands.START_MINPOOL):].split()
                            
                            z1 = int(z[0])
                            z2 = int(z[1])
                    else:        
                        #client sends his/her name
                        if message.startswith(commands.HELLO):
                            
                            name = message[len(commands.HELLO):].strip()
                            
                            #add name to list of clients
                            if name not in list_of_clients.values():
                                list_of_clients[conn] = name
                                
                                print("{} picked the following name: {}".format(addr[0], name))
                            else:
                                #if name is already in list of clients, send an error message to client
                                conn.send((commands.ERROR_NAME).encode())
                        else:
                            name = list_of_clients[conn] + " (" + addr[0] + ")"
                            
                            if message.startswith(commands.SEND_POW):
                                #client sent a solution for the proof of work assignment
                                counter += 1
                                
                                #set winner to the first miner
                                if winner == None:
                                    winner = conn
                                
                                h = message[len(commands.SEND_POW):].strip(commands.DELIM)
                                print("{} found hash {}".format(name, h))
                                
                                #checks if all clients have sent their proof of work. Works only if all clients maintain their connection with the server during the whole period.
                                if counter == len(list_of_clients)-1:
                                    print()
                                    print("{} wins the proof of work competition, congratulations!".format(list_of_clients[winner]))
                            elif message.startswith(commands.SEND_MINPOOL):
                                #client sent a solution for the mining pool

                                h = message[len(commands.SEND_MINPOOL):].strip(commands.DELIM)
                                
                                #only print the client's solution if it's still in time, i.e. another miner didn't just send a winning hash
                                if not found:
                                    print("{} found hash {}".format(name, h))
                                
                                #check if hash h starts with z1 or z2 zeros
                                if h.startswith("".join(["0"]*z1)):
                                    #client's hash h starts with z1 zeros, which means the mining pool has found its hash and the pool ends
                                    found = True
                                    incr_client_minpool(conn)
                                    
                                    print()
                                    print("A hash starting with {} zeros has been found by {}".format(z1, name))
                                    print()
                                    
                                    #split reward according to the amount of hashes all clients sent
                                    print("List of rewards:")
                                    print()
                                    print("Name \t \t Nr of hash submits \t Reward ({})".format(reward))
                                    
                                    total_hashes = sum(mining_pool.values())
                                    
                                    for client in mining_pool:
                                        print("{} \t \t {} \t \t \t {}".format(list_of_clients[client], mining_pool[client], (mining_pool[client]/total_hashes)*reward))
                                    
                                    #compute and prints elapsed time
                                    elap = time.time()-start
                                    m, s = divmod(elap, 60)
                                    print()
                                    print("Total time elapsed: {} min and {} s".format(m, s))
                                    print()
                                elif h.startswith("".join(["0"]*z2)):
                                    #client found a hash starting with z2 zeros, which means he sent a proof that he's still working hard on the problem
                                    #increment client's amount for every time they send in valid hashes.
                                    if not found:
                                        conn.send((commands.CONT_MINPOOL).encode())
                                        
                                        incr_client_minpool(conn)
                                    else:
                                        #sometimes it occures that another miner found a winning hash just fractions of seconds earlier and the poolmaster didn't broadcast the pool ending message yet, so that another miner still sent in a hash. Server will send a sorry message
                                        msg_sorry = "Sorry, your last hash was rejected, since another miner just found a hash starting with {} zeros".format(z1)
                                        conn.send(msg_sorry.encode())
                else:
                    #if the message is empty, the connection might have been broken, so in that case remove the client from list_of_clients
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

#remove client from list_of_cients
def remove(conn):
    if conn in list_of_clients:
        del list_of_clients[conn]
        print("{} disconnected".format(addr[0]))

#increment the amount of valid hashes a miner sent in
def incr_client_minpool(conn):
    if mining_pool.get(conn) == None:
        mining_pool[conn] = 1
    else:
        mining_pool[conn] += 1   

#reset the proof of work game
def reset_pow():
    global winner
    global counter
    
    winner = None
    counter = 0

#reset the mining pool game
def reset_minpool():
    global mining_pool
    global z1
    global z2
    global found
    global start
    
    mining_pool = {}
    z1 = -1
    z2 = -1
    found = False
    start = 0

#function to print titles before each pow/mining pool game
def print_title(title):
    print()
    print("-----------")
    print(title)
    print("-----------")
    print()
 
while True:
    #accepts a connection request
    #conn = socket object for client, addr is client's ip address
    conn, addr = server.accept()
 
    #server keeps dictionary structure of clients with names as values (default = "", clients can set their own names once they're connected)
    list_of_clients[conn] = ""
 
    #prints the address of the user that just connected
    print("{} connected".format(addr[0]))
 
    #creates an individual thread for every user that connects
    start_new_thread(clientthread,(conn,addr))
 
conn.close()
server.close()

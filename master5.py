#master
import socket
import select
import sys
import commands
import proofofwork

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#checks if enough input arguments have been given
if len(sys.argv) != 3:
    print("Correct usage: master.py, <ip address>, <port number>")
    exit()
    
ip = str(sys.argv[1])
port = int(sys.argv[2])

server.connect((ip, port))

#make self known to server
msg_hello = commands.HELLO + "master"
server.send(msg_hello.encode())

print("Welcome Master!")
 
while True:
    #maintains a list of possible input streams
    sockets_list = [sys.stdin, server]
 
    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])
    
    #let the master send a command to the miners (via the server)
    msg_master = input()
 
    for socks in read_sockets:
        if socks == server:
            #print server message
            msg_server = socks.recv(2048)
            print(msg_server)
        else:
            #master sent a message himself
            if msg_master == commands.START_POW:
                #master inserted command to start proof of work
                z = input("How many zeros should the client's hash start with? ")
    
                if not z == None:
                    msg_startpow = commands.START_POW + commands.DELIM + z
                    server.send(msg_startpow.encode())
                else:
                    print("An error occured while inserting z. Please try again.")
            elif msg_master == commands.START_MINPOOL:
                #master inserted command to start mining pool
                z1 = input("How many zeros should the hash start with? ")
                z2 = input("How many zeros should the client try to find? ")
    
                if not z1 == None and not z2 == None:
                    msg_startminpool = commands.START_MINPOOL + commands.DELIM + z1 + commands.DELIM + z2
                    server.send(msg_startminpool.encode())
                else:
                    print("An error occurred while inserting z1 and z2. Please try again.")

server.close()

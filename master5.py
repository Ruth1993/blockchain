# Python program to implement client side of chat room.
import socket
import select
import sys
import commands
import proofofwork

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 3:
    print("Correct usage: script, IP address, port number")
    exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.connect((IP_address, Port))
msg_hello = commands.HELLO + "master"
server.send(msg_hello.encode())

print("Welcome Master!")
 
while True:
 
    # maintains a list of possible input streams
    sockets_list = [sys.stdin, server]
 
    """ There are two possible input situations. Either the
    user wants to give  manual input to send to other people,
    or the server is sending a message  to be printed on the
    screen. Select returns from sockets_list, the stream that
    is reader for input. So for example, if the server wants
    to send a message, then the if condition will hold true
    below.If the user wants to send a message, the else
    condition will evaluate as true"""
    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])
    
    
    print("Please insert your commands: ")
    msg_master = input()
 
    for socks in read_sockets:
        if socks == server:
            msg_server = socks.recv(2048)
            print(msg_server)
        else:
            if msg_master == commands.START_POW:
                z = input("How many zeros should the client's hash start with?")
    
                msg_startpow = commands.START_POW + commands.DELIM + z
                server.send(msg_startpow.encode())
            elif msg_master == commands.START_MINPOOL:
                z1 = input("How many zeros should the hash start with? ")
                z2 = input("How many zeros should the client try to find? ")
    
                msg_startminpool = commands.START_MINPOOL + commands.DELIM + z1 + commands.DELIM + z2
                server.send(msg_startminpool.encode())
            
            print("<You>" + msg_master)

server.close()

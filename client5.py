# Python program to implement client side of chat room.
import socket
import select
import sys
import commands
import proofofwork

def send_name():
    name = input("Please insert your name: ")
    msg_hello = commands.HELLO + name
    server.send(msg_hello.encode())

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if len(sys.argv) != 3:
    print("Correct usage: script, IP address, port number")
    exit()
    
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])

server.connect((IP_address, Port))

print(commands.WELCOME)

send_name()
 
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
 
    for socks in read_sockets:
        if socks == server:
            data = socks.recv(2048).decode("utf-8")
            print(data)
            
            if data == commands.ERROR_NAME:
                #server sent an error message about the name
                print("Your name has already been chosen. Please pick another name.")
                send_name()
            elif data.startswith(commands.START_POW) == True:
                #master sent command to start proof of work assignment
                print("Master started the proof of work assignment")

                z = int(data[len(commands.START_POW):].strip()) #take the remaining part of the command as the amount of zeros
                h = proofofwork.gen_attempt(z) #found hash h
                send_pow = commands.SEND_POW + commands.DELIM + h
                server.send(send_pow.encode())
            elif data.startswith(commands.START_MINPOOL) == True:
                #master sent command to start mining pool assignment
                print("mining pool started")

server.close()

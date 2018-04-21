# Python program to implement client side of chat room.
import socket
import select
import sys
import commands
import proofofwork

#function to choose name and send this name to the server
def send_name(name):
    msg_hello = commands.HELLO + name
    server.send(msg_hello.encode())

#function to send solution for the mining pool to the server
def send_sol_minpool():
    h = proofofwork.gen_attempt(z2)
    send_minpool = commands.SEND_MINPOOL + commands.DELIM + h
    server.send(send_minpool.encode())

#sserver variable
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#checks if enough input arguments have been given
if len(sys.argv) != 4:
    print("Correct usage: client.py, <ip address>, <port number>, <name>")
    exit()
    
ip = str(sys.argv[1])
port = int(sys.argv[2])
name = str(sys.argv[3])

#connect to server using ip address and port extracted from the command line
server.connect((ip, port))

#print a welcome message for the client
print(commands.WELCOME)

#immediately after the client has been connected to the server, enter name and also send this to the server
send_name(name)

#maintain list of mining pool variables
#z1 is the amount of zeros for the hash that the mining pool needs to find
#z2 is the amount of zeros for the hash that miners can send it to prove that they're working hard on the problem
z1 = -1
z2 = -1
 
while True:
    #maintains a list of possible input streams
    sockets_list = [sys.stdin, server]
 
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

                z = int(data[len(commands.START_POW):].strip(commands.DELIM)) #take the remaining part of the command as the amount of zeros
                h = proofofwork.gen_attempt(z) #found hash h
                send_pow = commands.SEND_POW + commands.DELIM + h
                server.send(send_pow.encode())
            elif data.startswith(commands.START_MINPOOL) == True:
                #master sent command to start or continue mining pool assignment
                print("Master started the mining pool")
                
                z = data[len(commands.START_MINPOOL):].split() #take the remaining part of the command as the amount of zeros
                z1 = int(z[0])
                z2 = int(z[1])
                
                send_sol_minpool()
            elif data.startswith(commands.CONT_MINPOOL):
                print("Thanks for your solution! Please compute another solution")
                send_sol_minpool()
                


server.close()

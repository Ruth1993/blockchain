# Python TCP Client A
import socket 
import proofofwork
import commands

host = socket.gethostname() 
port = 1247
BUFFER_SIZE = 2000 
 
tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpClientA.connect((host, port))
name = input("Enter your name: ")
tcpClientA.send(("I'm host " + host + " with port " + str(port) + " and my name is " + name).encode())
print("Wait until the server sends you a challenge. In the meanwhile, sit back, relax and take a beer :)")

while True:
    data = (tcpClientA.recv(BUFFER_SIZE)).decode("utf-8")
    print(data)
    if data.startswith(commands.PROBLEM_POW) == True:
        print("pow wordt herkend")
        #server sent command to start proof of work assignment
        z = data[len(commands.PROBLEM_POW):] #take the remaining part of the command as the amount of zeros
        proofofwork.gen_attempt(z)
    else:
        print("pow wordt niet herkend")

tcpClientA.close()

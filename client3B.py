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
send_name = commands.HELLO + name
tcpClientA.sendto(send_name.encode(), (host, port))
print("Wait until the server sends you a challenge. In the meanwhile, sit back, relax and take a beer :)")

while True:
    data = (tcpClientA.recv(BUFFER_SIZE)).decode("utf-8")

    print(data)
    if data.startswith(commands.START_POW) == True:
        #server sent command to start proof of work assignment

        z = int(data[len(commands.START_POW):].strip()) #take the remaining part of the command as the amount of zeros
        h = proofofwork.gen_attempt(z) #found hash h
        send_pow = name + " on ip " + commands.SEND_POW + commands.DELIM + h
        tcpClientA.sendto(send_pow.encode(), (host, port))
    elif data.startswith(commands.START_MINPOOL) == True:
        print("minpool started")
    elif not data == "":
        print("Error")
        break;
    else:
        #client received een lege string aan data als een andere client connect, hellup :(
        poep = 5
        
tcpClientA.close()

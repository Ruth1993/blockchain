import commands
import time
import socket
from threading import Thread 
from socketserver import ThreadingMixIn 

# Multithreaded Python server : TCP Server Socket Thread Pool
class ClientThread(Thread): 
 
    def __init__(self,ip,port): 
        Thread.__init__(self) 
        self.ip = ip 
        self.port = port 
        print(str(time.time()) + ": [+] New server socket thread started for " + ip + ":" + str(port))
 
    def run(self): 
        while True : 
            data = conn.recv(2048).decode("utf-8")
            
            print(str(time.time()) + ": Server received data: ", data)

            if data.startswith(commands.HELLO):
                #nog even niks
                test = 3
            elif data.startswith(commands.SEND_POW):
                #check if hash is okay?
                test = 5

            message = input(commands.MSG_SERVER)
            
            if message == commands.EXIT:
                break
            elif message == commands.START_POW:
                z = input("How many zeros should the client's hash start with? ")
                send_pow = commands.START_POW + commands.DELIM + z
                conn.send(send_pow.encode())
            elif message == commands.START_MINPOOL:
                z1 = input("How many zeros should the hash start with? ")
                z2 = input("How many zeros should the client try to find? ")
                send_minpool = commands.START_MINPOOL + commands.DELIM + z1 + commands.DELIM + z2
                conn.send(send_minpool.encode())
            else:
                print("Wrong input. Please try again.")
                message = input(commands.MSG_SERVER)
  

# Multithreaded Python server : TCP Server Socket Program Stub
TCP_IP = '0.0.0.0' 
TCP_PORT = 1247 
BUFFER_SIZE = 20  # Usually 1024, but we need quick response 

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
tcpServer.bind((TCP_IP, TCP_PORT)) 
threads = []
 
while True: 
    tcpServer.listen(4) 
    (conn, (ip,port)) = tcpServer.accept() 
    newthread = ClientThread(ip,port) 
    newthread.start() 
    threads.append(newthread)
 
for t in threads: 
    t.join() 

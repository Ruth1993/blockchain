import commands
import socket 
from threading import Thread 
from socketserver import ThreadingMixIn 

# Multithreaded Python server : TCP Server Socket Thread Pool
class ClientThread(Thread): 
 
    def __init__(self,ip,port): 
        Thread.__init__(self) 
        self.ip = ip 
        self.port = port 
        print("[+] New server socket thread started for " + ip + ":" + str(port))
 
    def run(self): 
        while True : 
            data = conn.recv(2048) 
            print("Server received data:", data)
            MESSAGE = input("Enter server message: ")
            if MESSAGE == commands.EXIT:
                break
            elif MESSAGE == commands.START_POW:
                z = input("How many zeros should the client's hash start with? ")
                send_pow = commands.START_POW + " " + z
                conn.send(send_pow.encode())
            elif MESSAGE == commands.START_MINPOOL:
                z1 = input("How many zeros should the hash start with? ")
                z2 = input("How many zeros should the client try to find? ")
                problem = "Find hash starting with " + z1 + " zeros. But first try to find " + z2 + " zeros"
                conn.send(problem.encode())
            else:
                input("Wrong input. Please try again.")
  

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
    #print("Connection with", )
 
for t in threads: 
    t.join() 

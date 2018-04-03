# Python TCP Client B
import socket 

host = socket.gethostname() 
port = 2004
BUFFER_SIZE = 2000 
MESSAGE = input("tcpClientB: Enter message/ Enter exit:")

while MESSAGE != 'exit':
    tcpClientB = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    tcpClientB.connect((host, port))
    tcpClientB.send(MESSAGE.encode())     
    data = tcpClientB.recv(BUFFER_SIZE)
    print(" Client received data:", data)
    MESSAGE = input("tcpClientB: Enter message to continue/ Enter exit:")
    tcpClientB.close() 

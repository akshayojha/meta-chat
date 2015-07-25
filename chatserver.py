"""
Python2.7 Chat Server v0.5
Starts a telnet chat server on given host and port
Can handle multiple connections
"""
#For sockets
import socket
#For exit
import sys
#For threading
from thread import *
#Try to create IPV4 TCP socket
try:
    server_sock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Handle exception
except socket.error, msg:
    print "Error creating socket: "+str(msg)
    sys.exit()
#Indicate socket creation success
print "Successfully created socket!"
#Server on localhost
host="127.0.0.1"
#Get host and port from user
host_port=int(raw_input("Enter port:"))
#Bind socket to given host and port
try:
    server_sock.bind((host, host_port))
except socket.error, msg:
    print "Error binding socket to given host: "+str(msg)
    sys.exit()
print "Binding established!"
#Start listening on the given port
server_sock.listen(backlog)
print "Meta Chat Server started!"
print "Waiting for clients..."

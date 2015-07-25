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
#Get host andport from user
host_port=int(raw_input("Enter port:"))
#Max number on non-accepted connections
backlog=5
recv_size=4096
connections=[server_sock]

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
def getNick(client):
    nick_msg="Welcome! Enter your nick and press enter: "
    client.sendall(nick_msg)
    nick=str(client.recv(recv_size))
    nick=nick[:nick.rfind('\n')]
    print nick
    return nick

def handleClient(client):
#Send acknowledgment to client
    name=getNick(client)
    while True:
        msg=str(client.recv(recv_size))
        msg=msg[:msg.rfind('\n')]
        msg=name+"->"+msg
        print msg
        for conn in connections:
            if conn !=client and conn!=server_sock:
                try:
                    conn.sendall(msg)
                except:
                    conn.close()
                    connections.remove(conn)
#Close connection with client
    client.close()    

while True:
#Accept connection from client
    client, client_addr =server_sock.accept()
    connections.append(client)
    print "Connected to "+client_addr[0]+":"+str(client_addr[1])
    start_new_thread(handleClient, (client,))

#Close socket to terminate connection
server_sock.close()

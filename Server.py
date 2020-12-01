import socket
import os
from _thread import *
import time

# Clears socket of data
def ClearData(toClearSocket):
	while True:
		try:
			PacketBytes = toClearSocket.__Listener.recv(1024)
		except:
			break;
			
#Prompts the user to enter a valid IP
def GetValidIP():
	try:
		input_ip = input("What is the IP of the host you'd like to find?")
		socket.inet_aton(input_ip)
		return input_ip
	except socket.error:
		print("Invalid IP. Please try again.")
				
#variables
ServerSocket = socket.socket()
host = '127.0.0.1'
port = 1233
ThreadCount = 0
jobs = 3

try:
	ServerSocket.bind((host, port))
except socket.error as e:
	print(str(e))

print('PLEASE NOTE!')
print('This program will not function if you have not installed SCAPY!')

print('Waiting for a Connection..')
ServerSocket.listen(5)

#send to seeker
def threaded_client(connection):
	currentJob = -1; #indicates which job was selected by the seeker
	jobCounter = 0
	while True:
		connection.send(str.encode('\n\nWhich job would you like to do? \n1: Detect the status of a given port at a given IP. \n2: Detect if a given host is online or not. \n3: TCP SYN Flood attack\n4: UDP Flood\nPlease enter 1, 2, 3 or 4.\n> '))
		data = connection.recv(1024)
		if data.decode('utf-8')=='1':
			currentJob = 1;
			ipToSend = '127.0.0.1'
			portToSend = '133'
			print("Checking port #", portToSend, "on IP " + ipToSend)
			jobCounter = jobCounter+1
			reply = '\nJob 1 Given.'
				
		elif data.decode('utf-8')=='2':
			currentJob = 2;
			hostAddr = GetValidIP()
			print("\nAddress sent: " + hostAddr)
			jobCounter = jobCounter+1
			reply = '\nJob 2 Given.'
			   
		elif data.decode('utf-8')=='3':
			reply = '\nJob 3 Given.'
			jobCounter = jobCounter+1
			#reply = '\nJob 2 Given.'
		
		elif data.decode('utf-8')=='4':
			jobCounter = jobCounter+1
			reply = '\nJob 4 Given.'
		
		else:
			reply = '\nJob Not Given.'
		
		if jobCounter == 3:
			break
		connection.send(str.encode(reply))
		
		if (currentJob == 1): #check ip at port
			connection.send(str.encode(ipToSend))
			connection.recv(1024) #This is just to wait for confirmation from client
			ClearData(connection)
			connection.send(str.encode(portToSend))
			print(connection.recv(1024).decode('utf-8'))	#The result
		
		elif (currentJob == 2): #If job 2 was selected, send the address to find
			connection.send(str.encode(hostAddr))
			print(connection.recv(1024).decode('utf-8'))	#The result
		
		elif (currentJob == 3):
			#tcp flood?
			pass #delete this once done
			
		elif (currentJob == 4):
			#udp flood?
			pass #delete this once done
			
	connection.close()

#print on server
while True:
	Client, address = ServerSocket.accept()
	print('Connected to: ' + address[0] + ':' + str(address[1]))
	start_new_thread(threaded_client, (Client, ))
	ThreadCount += 1
	print('Thread Number: ' + str(ThreadCount))
ServerSocket.close()

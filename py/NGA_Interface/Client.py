import socket, subprocess, struct

class NGA_Interface_Client:

	server_addr = 'localhost'
	server_port = 31001
	server_executable = "start  /min \"\" ..\\bin\\FlyCap2Daemon.exe"
	connected = 0
	dog_score = 0

	def __init__(self):
		self.startDaemon()
                j = 1
		
	def startDaemon(self):
		self.p = subprocess.Popen(self.server_executable, shell=True)

	def connect(self):
                self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.client_sock.connect((self.server_addr, self.server_port))
		self.connected = 1


	def send(self,command):
		try:
			#print "bytes sent: %d" %
                        self.client_sock.send(command)
		except socket.error, e:
			print "connection error %s \n" % e
			
	def readCam(self):
		try:
			self.myint = self.client_sock.recv(4)
			self.numCameras = struct.unpack("<i", self.myint)[0]
		except socket.error, e:
			print "connection error %s \n" % e

	def readIm(self):
		try:
			self.myint = self.client_sock.recv(4)
		except socket.error, e:
			print "connection error %s \n" % e

        def readDog(self):
		try:
			self.myint = self.client_sock.recv(256)
			self.dog_score = self.myint
		except socket.error, e:
			print "connection error %s \n" % e			

	def close(self):
		self.client_sock.close()
		self.connected = 0

	def kill(self):
		self.p.kill()

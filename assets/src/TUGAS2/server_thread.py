from socket import *
import socket
import threading
import logging
import time
import sys
from datetime import datetime

class ProcessTheClient(threading.Thread):
	def __init__(self,connection,address):
		self.connection = connection
		self.address = address
		threading.Thread.__init__(self)

	# def run(self):
	# 	while True:
	# 		data = self.connection.recv(32)
	# 		if data:
	# 			self.connection.sendall(data)
	# 		else:
	# 			break
	# 	self.connection.close()
	
	# INI UNTUK POIN C
	
	def run(self):
		while True:
			data = self.connection.recv(1024)
			if not data:
				break
			logging.warning(f"Raw data dari client: {data} ({list(data)})")  # log byte
			message = data.decode()
			# Respons hanya jika diakhiri \r\n
			if message.endswith("\r\n"):
				self.connection.sendall(b"DITERIMA\r\n")
			else:
				self.connection.sendall(b"DITOLAK: Tidak diakhiri CRLF\r\n")
			if message.strip() == "QUIT":
				break

	# INI UNTUK POIN D
	
	# def run(self):
	# 	while True:
	# 		data = self.connection.recv(1024)
	# 		if not data:
	# 			break

	# 		logging.warning(f"Raw data dari client: {data} ({list(data)})")  # Tambahan ini

	# 		message = data.decode()
	# 		if message.startswith("TIME") and message.endswith("\r\n"):
	# 			now = datetime.now()
	# 			response = now.strftime("JAM %d %m %y %H:%M:%S\r\n")
	# 			self.connection.sendall(response.encode())

	# 		elif message.startswith("QUIT") and message.endswith("\r\n"):
	# 			self.connection.sendall(b"Goodbye\r\n")
	# 			break

	# 		else:
	# 			self.connection.sendall(b"ERROR: Format tidak dikenali\r\n")

	# 	self.connection.close()
        


class Server(threading.Thread):
	def __init__(self):
		self.the_clients = []
		self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		threading.Thread.__init__(self)

	def run(self):
		self.my_socket.bind(('0.0.0.0',8889))
		self.my_socket.listen(1)
		while True:
			self.connection, self.client_address = self.my_socket.accept()
			logging.warning(f"connection from {self.client_address}")
			
			clt = ProcessTheClient(self.connection, self.client_address)
			clt.start()
			self.the_clients.append(clt)
	

def main():
	svr = Server()
	svr.start()

if __name__=="__main__":
	main()

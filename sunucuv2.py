import socket
import threading
import time


class Sunucu:

	def __init__(self):
		self.sock = None
		self.cons = []

	def SERVER(self):
		self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.sock.bind(("localhost",1331))
		self.sock.listen(10)

		while True:
			con, addr = self.sock.accept()

			if con:

				self.cons.append(con)

				print(addr,"Bağlandı.")

				t3 = threading.Thread(target=serv.GAIN_DATA,args= (con,addr) )
				t3.start()


	def GAIN_DATA(self,con,adres,*ignore):

		print(adres)
		while True:
			data = con.recv(2048)

			if data:
				print(data)
				serv.BROADCAST(str(data))

	def BROADCAST(self,mesaj):
		for i in self.cons:
			i.sendall(mesaj.encode("utf-8"))

serv = Sunucu()


def Arayuz():
	while True:
		girdi = input("-> ")

		kg = girdi.lower()

		if "server" in kg:
			if "start" in kg:
				time.sleep(1)

				t1 = threading.Thread(target=serv.SERVER)
				t1.start()

				print("Server Aktif")
			elif "stop" in kg:
				pass

		elif "exit" in kg:
			exit()

t2 = threading.Thread(target=Arayuz)
t2.start()


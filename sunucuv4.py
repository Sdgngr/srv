import socket as s
import threading
import random
import time

kodListe = []
ipListe = []
portListe = []

class Oturum:
	def __init__(self,_IP,_PORT,_ID):
		self.s = s.socket(s.AF_INET, s.SOCK_STREAM)
		self.s.bind((_IP,_PORT))
		self.s.listen(10)
		self.kapaliMi = False
		self.ilkMi = True
		self.id = _ID
		self.ip = _IP
		self.port = _PORT
		self.conListe = []
		self.mesajlar = []
		self.yetkiliListe = []
		self.kullanicilar = []
		self.kullaniciSayi = 0
		self.eklendiMi = False
		th1 = threading.Thread(target = Oturum.ACC,args = (self,"w"))
		th1.start()

	def ACC(self,*ignore):

		while True:
			if self.kapaliMi != True:
				try:
					con,addr = self.s.accept()
					print(self.id," : ",addr," Bağlandı.")
					self.conListe.append(con)
					th2 = threading.Thread(target = Oturum.GAIN,args = (self,con,addr))
					th2.start()
				except ConnectionAbortedError:
					break
			else:
				break

	def GAIN(self,con,addr):
		self.kullaniciSayi = self.kullaniciSayi + 1

		while True:

			data = con.recv(2048).decode("utf-8")

			if data != "": 
				if "#~kln" in data:
					print("kullanci")
					kullaniciAdi = data[5:].strip()
					Oturum.SEND_P(self,con)
					for i in self.conListe:
						i.sendall(("SİSTEM : "+ kullaniciAdi + " Oturuma Katıldı.").encode("utf-8"))
					self.kullanicilar.append(kullaniciAdi)
					if self.ilkMi == True:
						print("Eklendi!")
						self.yetkiliListe.append(kullaniciAdi)
						self.ilkMi = False
							
				elif "/" in data:
					if kullaniciAdi in self.yetkiliListe:
						if "/admin" in data:
							if data[7:] in self.kullanicilar:
								self.eklendiMi = True

							if self.eklendiMi == True:
								for i in self.conListe:
									 i.sendall(("SİSTEM : "+data[7:]+" Yönetici Yapıldı.").encode("utf-8"))
								self.eklendiMi = False

							else:
								con.sendall("SİSTEM : Kullanıcı Bulunamadı.".encode("utf-8"))
						elif "/ban" in data:
							for i in self.conListe:
								i.sendall(("#~bn"+data[5:]).encode("utf-8"))

					else:
						con.sendall("SİSTEM : Bu Komutu Kullanmak İçin Yetkiniz Yok!".encode("utf-8"))
				else:
					Oturum.BROADCAST(self,con,data,kullaniciAdi)
			else:
				self.kullaniciSayi = self.kullaniciSayi - 1
				print("Çıkış Yapıldı.")
				if self.kullaniciSayi == 0:
					print("Kullanıcı Sayısı 0. Oturum Kapatıldı.")

					kodListe.remove(self.id)
					ipListe.remove(self.ip)
					portListe.remove(str(self.port))

					self.kapaliMi = True

					self.s.close()
				break
			
	def BROADCAST(self,con,data,kullaniciAdi):
		self.mesajlar.append(kullaniciAdi+" : " +data)
		print(self.mesajlar)

		for i in self.conListe:
			i.sendall((kullaniciAdi+" : " +data).encode('utf-8'))
	def SEND_P(self,con):
		for i in self.mesajlar:
			con.sendall(i.encode("utf-8"))
			time.sleep(0.01)

########################################################################################################################

class Sunucu:

	def __init__(self,host,port):
		self.portlar = []
		self.sock = s.socket(s.AF_INET,s.SOCK_STREAM)
		self.sock.bind((host,port))
		self.sock.listen(10)

		th = threading.Thread(target = Sunucu._ACC,args = (self,"w"))
		th.start()

	def _ACC(self,*ignore):
		while True:
			con,addr = self.sock.accept()
			print(str(addr) + " Bağlandı.")
			th2 = threading.Thread(target= Sunucu._DATA,args = (self,con,addr))
			th2.start()

	def oturumGonder(self,con,ism):
		
		kodlar = ""

		for i in kodListe:
			if i.strip() != "":
				kodlar = kodlar + (i + "~")

		con.sendall((ism+kodlar).encode("utf-8"))

	def _DATA(self,con,addr):
		x = None
		
		while True:
			data = con.recv(2048).decode("utf-8")
			if data:
				print(data)
				if "#~olstr" in data :
					print(data)
					while True:
						if x not in self.portlar:
							x = random.randint(1000,1331)
							self.portlar.append(x)
							break
						else:
							pass

					idd = data[7:]
					con.sendall(("#~blg"+"localhost"+":"+str(x)).encode("utf-8"))

					kodListe.append(idd)
					ipListe.append("localhost")
					portListe.append(str(x))

					otr = Oturum("localhost",x,idd)
				elif "#~grs" in data:
					for i in range(len(kodListe)):
						if data[5:] == kodListe[i]:
							hst = ipListe[i]
							prt = portListe[i]

							print(hst+":"+prt)

							con.sendall(("#~dgru"+hst+":"+prt).encode("utf-8"))
						else:
							con.sendall(("#~ynls".encode("utf-8")))
				elif "#~ynotr" in data:
					Sunucu.oturumGonder(self,con,"#~ynotrm")
				elif "#~otr" in data:
					Sunucu.oturumGonder(self,con,"#~otrmlr")

sunucu = Sunucu("localhost",1332)

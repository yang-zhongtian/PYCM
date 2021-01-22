import socket
import time
import struct
from DirFix import *
from Public.Packages import NetworkDiscoverFlag

class StudentLogin(object):
	socket_ip = None
	socket_port = None
	socket_server = None
	discover_interval = None
	def __init__(self, socket_ip, socket_port, client_name, client_ip, client_mac, discover_interval=5):
		self.socket_ip = socket_ip
		self.socket_port = socket_port
		self.client_name = str(client_name)
		self.client_ip = client_ip
		self.client_mac = str(client_mac)
		self.discover_interval = discover_interval
		self.__init_socket_server()
	def __init_socket_server(self):
		self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		self.socket_server.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)
		self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket_server.bind(('', self.socket_port))
		self.socket_server.setsockopt(
			socket.IPPROTO_IP,
			socket.IP_ADD_MEMBERSHIP,
			socket.inet_aton(self.socket_ip) + socket.inet_aton(self.client_ip)
		)
	def notify(self):
		try:
			socket_packet = struct.pack(
				'!i20s4s12s', NetworkDiscoverFlag.ClientFlag, self.client_name.encode(),
				socket.inet_aton(self.client_ip), self.client_mac.encode()
			)
			self.socket_server.sendto(socket_packet, (self.socket_ip, self.socket_port))
			return True
		except KeyboardInterrupt:
			self.socket_server.close()
			return
		except:
			return False

if __name__ == '__main__':
	A = StudentLogin('225.2.2.19', 4089, 'C1', '10.60.5.13', '6C0B84A4ED61')
	print(A.notify())
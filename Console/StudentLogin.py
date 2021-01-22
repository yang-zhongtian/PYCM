import socket
import struct
from DirFix import *
from Public.Packages import NetworkDiscoverFlag

class StudentLogin(object):
	current_ip = None
	socket_ip = None
	socket_port = None
	socket_client = None
	def __init__(self, current_ip, socket_ip, socket_port):
		self.current_ip = current_ip
		self.socket_ip = socket_ip
		self.socket_port = socket_port
		self.__init_socket_client()
	def __init_socket_client(self):
		self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		self.socket_client.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)
		self.socket_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket_client.bind(('', self.socket_port))
		self.socket_client.setsockopt(
			socket.IPPROTO_IP,
			socket.IP_ADD_MEMBERSHIP,
			socket.inet_aton(self.socket_ip) + socket.inet_aton(self.current_ip)
		)
	def __client_found_handler(self, client_name, client_ip, client_mac):
		print(client_name, client_ip, client_mac)
	def wait_for_client(self):
		try:
			while True:
				try:
					socket_data, socket_addr = self.socket_client.recvfrom(1024)
					client_flag, client_name, client_ip, client_mac = struct.unpack('!i20s4s12s', socket_data)
					if client_flag == NetworkDiscoverFlag.ClientFlag:
						client_name = client_name.strip(b'\x00').decode()
						client_ip = socket.inet_ntoa(client_ip)
						client_mac = client_mac.decode()
						if client_ip == socket_addr[0]:
							self.__client_found_handler(client_name, client_ip, client_mac)
				except Exception as e:
					print(e)
		except KeyboardInterrupt:
			self.socket_server.close()
			return None

if __name__ == '__main__':
	A = StudentLogin('10.60.5.13', '225.2.2.19', 4089)
	print(A.wait_for_client())
import socket
import time
import struct
from DirFix import *
from Public.Packages import NetworkDiscoverFlag

class NetworkDiscover(object):
	socket_ip = None
	socket_port = None
	socket_server = None
	discover_interval = None
	def __init__(self, socket_ip, socket_port, discover_interval=5):
		self.socket_ip = socket_ip
		self.socket_port = socket_port
		self.discover_interval = discover_interval
		self.__init_socket_server()
	def __init_socket_server(self):
		self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		self.socket_server.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)
		self.socket_server.setsockopt(
			socket.IPPROTO_IP,
			socket.IP_ADD_MEMBERSHIP,
			socket.inet_aton(self.socket_ip) + socket.inet_aton('0.0.0.0')
		)
	def start(self):
		try:
			socket_packet = struct.pack('!i', NetworkDiscoverFlag.ConsoleFlag)
			while True:
				self.socket_server.sendto(socket_packet, (self.socket_ip, self.socket_port))
				time.sleep(self.discover_interval)
		except KeyboardInterrupt:
			self.socket_server.close()
			return

if __name__ == '__main__':
	A = NetworkDiscover('224.50.50.50', 4088, 1)
	A.start()
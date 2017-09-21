# Taken from https://stackoverflow.com/a/17668009

import struct

def send_msg(sock, msg):
	msg = struct.pack('>I', len(msg)) + msg
	sock.sendall(msg)

def recv_msg(sock):
	raw_msglen = recvall(sock, 4)

	if not raw_msglen:
		return None

	msglen = struct.unpack('>I', raw_msglen)[0]

	return recvall(sock, msglen)

def recvall(sock, n):
	data = b''

	while len(data) < n:
		packet = sock.recv(n - len(data))

		if not packet:
			return None

		data += packet

	return data
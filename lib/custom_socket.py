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

# Taken from https://stackoverflow.com/a/28950776
import socket

def find_own_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()

    return ip
import struct, socket, re, threading

# send_msg, recv_msg, recvall are taken from https://stackoverflow.com/a/17668009
# find_own_ip is taken from https://stackoverflow.com/a/28950776

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

import re, threading

def check_ip(ip, server):
	s = socket.socket()
	try:
		serv = s.connect_ex((ip, 11235))
	except socket.error:
		s.close()

	if serv == 0:
		server.append(s)


def find_server():
	own_ip = find_own_ip()
	base = re.match('(\d+\.\d+\.\d+\.)', own_ip).groups()[0]
	threads = []
	serv = []

	for i in range(0, 256):
		ip = base + str(i)
		threads.append(threading.Thread(target=check_ip, args=(ip, serv)))
		threads[i].start()

	for i in range(0, 256):
		threads[i].join()

	return serv[0]
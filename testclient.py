import socket, sys

sock = socket.socket()
sock.setblocking(True)
host = '192.168.1.7'
port = 12345

sock.connect((host, port))
print('Connected to the game on ', host, ':', str(port), '... Waiting for the opponent(s)...\n')

stdin = sock.makefile('r')
stdout = sock.makefile('w')

line = stdin.readline()
while line:
  print(line, end="")
  if line.strip().endswith(':'):
    answer = input('=>')
    stdout.write(answer + '\n')
    stdout.flush()
  line = stdin.readline()
sock.close()

import socket

sock = socket.socket()
sock.setblocking(True)
host = '192.168.1.7'
port = 12345

sock.connect((host, port))
print('Connected to the game on {}:{}... Waiting for the opponent(s)...\n'.format(host, port))

s_input = sock.makefile('r')
s_output = sock.makefile('w')

try:
  line = s_input.readline()

  while line:
    print(line, end="")
    if line.strip().endswith(':'):
      answer = input('=> ')
      s_output.write(answer + '\n')
      s_output.flush()
    line = s_input.readline()
finally:
  sock.close()

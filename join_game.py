import socket, sys

try:
  sock = socket.socket()
  sock.setblocking(True)

  host = sys.argv[1]
  port = 12345

  sock.connect((host, port))
  print('Connected to the game on {}:{}... Waiting for the opponent(s)...\n'.format(host, port))

  s_input = sock.makefile('r')
  s_output = sock.makefile('w')

  line = s_input.readline()

  while line:
    print(line, end="")

    if line.strip().endswith(':'):
      answer = input()
      s_output.write(answer + '\n')
      s_output.flush()

    line = s_input.readline()

  sock.close()
except IndexError:
  print('Usage: python3 join_game.py <ip_address>')

import struct, socket, re, threading, pickle

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

def check_ip(ip, server):
  s = socket.socket()

  try:
    val = s.connect_ex((ip, 11235))
  except socket.error:
    s.close()

  if val:
    s.close()

  # connect_ex returns 0 if socket connects
  if val == 0:
    server.append(s)

def find_server():
  own_ip = find_own_ip()
  # ip address except for the last number
  base = re.match('(\d+\.\d+\.\d+\.)', own_ip).groups()[0]
  # Use threads to make it faster
  threads = []
  # serv is an array in order to modify it in another method
  serv = []

  # Check all the possible ips in range
  for i in range(0, 256):
    ip = base + str(i)
    threads.append(threading.Thread(target=check_ip, args=(ip, serv)))
    threads[i].start()

  # Join threads to wait all to finish before returning
  for i in range(0, 256):
  	threads[i].join()

  if serv:
  	return serv[0]
  else:
  	return None

def create_lan_game(options, queue, bag):
  # Server goes first
  own_mark = 0
  cur_play_mark = 0

  game_online = True
  lan_players = []
  play_num = options['play_num']

  server = socket.socket()

  server.bind(('', 11235))
  server.listen()

  # Let players join the game and add their names into options before
  # serving them the options .The range starts from 1 because it doesn't
  # include the player initializing the server.
  for i in range(1, options['play_num']):
    cli, addr = server.accept()
    lan_players.append(cli)
    name = pickle.loads(recv_msg(cli))
    options['names'].append(name)

  # m is each joined player's mark to determine their turn
  for m, pl in enumerate(lan_players):
    send_msg(pl, pickle.dumps((options, m + 1)))

  # Flag for initializing players
  queue.put(True)

  # Wait till queue is empty so that the same flag won't be returned.
  while not queue.empty():
    continue

  players = queue.get()

  for pl in lan_players:
    send_msg(pl, pickle.dumps((players, bag)))

  while game_online:
    if cur_play_mark != own_mark:
      # - 1 because lan_players array size is play_num - 1
      player = lan_players[cur_play_mark - 1]

      turn_pack = recv_msg(player)

      # Prevent the own turn_pack to be put in the queue
      if turn_pack and turn_pack[0] != own_mark:
        queue.put(pickle.loads(turn_pack))

        game_online = pickle.loads(turn_pack)[-1]

        for mark, pl in enumerate(lan_players):
          # Prevent sending the received turn_pack to go back
          if mark != cur_play_mark - 1:
            send_msg(pl,turn_pack)

        # Wait till queue is empty so that the same turn_pack
        # isn't evaluated twice
        while not queue.empty():
          continue

        cur_play_mark = set_lan_cpm(cur_play_mark, turn_pack, play_num)
    else:
      if not queue.empty():
        turn_pack = queue.get()
        game_online = turn_pack[-1]

        for pl in lan_players:
          send_msg(pl, pickle.dumps(turn_pack))

        cur_play_mark = set_lan_cpm(cur_play_mark, turn_pack, play_num)

  server.close()

def join_lan_game(options, queue):
  cur_play_mark = 0
  game_online = True

  # Automatically detect server ip and connect to it
  # Server is None if no server is found
  server = find_server()

  if server:
    send_msg(server, pickle.dumps(options['names'][0]))

    options, own_mark = pickle.loads(recv_msg(server))
    queue.put((options, own_mark))

    play_num = options['play_num']

    players, bag = pickle.loads(recv_msg(server))
    queue.put((players, bag))

    while game_online:
      if own_mark == cur_play_mark:
        if not queue.empty():
          turn_pack = queue.get()
          game_online = turn_pack[-1]

          send_msg(server, pickle.dumps(turn_pack))

          cur_play_mark = set_lan_cpm(cur_play_mark, turn_pack, play_num)
      else:
        turn_pack = pickle.loads(recv_msg(server))
        game_online = turn_pack[-1]

        # If a player is not challenged, the first element of turn_pack is
        # a player's mark. This prevents accidentally receiving own turn_pack
        if turn_pack[0] != own_mark:
          queue.put(turn_pack)

          cur_play_mark = set_lan_cpm(cur_play_mark, turn_pack, play_num)

          while not queue.empty():
            continue

    server.close()
  else:
    queue.put(False)

def set_lan_cpm(cur_play_mark, turn_pack, play_num):
  # In challenge mode, if a player challenges a word, the second element
  # of the turn_pack is the flag for challenge succeeded or failed
  try:
    chal_check = pickle.loads(turn_pack)[1]
  except:
    chal_check = turn_pack[1]

  # Increase cur_play_mark by 1 if the player isn't challenged or
  # challenge didn't succeed.
  if type(chal_check) != type(True) or not chal_check:
    # cur_play_mark shouldn't be less than play_num
    return (cur_play_mark + 1) % play_num
  else:
    return cur_play_mark
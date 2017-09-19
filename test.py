  def create_server(self, options, queue, bag):
    mark = 0
    cur_play_mark = 0
    lan_players = []
    abled = True
    game_online = True

    ser = socket.socket()

    ser.bind(('', 11235))
    ser.listen()

    print('\nServer up and running...\n')

    for i in range(1, options['players']):
      cli, addr = ser.accept()
      lan_players.append(cli)
      name = cli.recv(1024)
      name = pickle.loads(name)
      options['names'].append(name)

      print('Connected by {}'.format(addr))

    options = pickle.dumps(options)

    for i, pl in enumerate(lan_players):
      pl.sendall(pickle.dumps((options, i + 1)))

    self.initialize_players()

    for st in lan_players:
      st.sendall(pickle.dumps((players, bag)))

    while game_online:
      if cur_play_mark != 0:
        source = lan_players[cur_play_mark]
        word = source.recv(1024)

        word = pickle.loads(word)

        for st in lan_players:
          st.sendall(pickle.dumps(word))

        queue.put(word)

        for st in lan_players:
          st.sendall(pickle.dumps(players))
        cur_play_mark = (cur_play_mark + 1) % options['players']
      else:
      	word = queue.get()

      	for st in lan_players:
      		st.sendall(pickle.dumps(word))
      		
        cur_play_mark = (cur_play_mark + 1) % options['players']

    ser.close()
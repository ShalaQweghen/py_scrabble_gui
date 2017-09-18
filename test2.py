  def handle_lan_game(self, options):
    host = '127.0.0.1'
    port = 11235

    sock = socket.socket()
    sock.connect((host, port))

    print('Connected to {}'.format(host))

    sock.sendall(pickle.dumps(options['names'][0]))

    options, self.mark = pickle.loads(sock.recv(1024))

    options = pickle.loads(options)
    options['joined'] = True

    self.resolve_options(options)
    self.set_variables()
    self.draw_main_frame()
    self.draw_info_frame()

    players, self.bag = pickle.loads(sock.recv(1024))
    self.players = players

    self.initialize_game()

    while self.game_online:
      if self.mark == self.cur_play_mark:
        if not self.word:
          self.enable_board()

        if self.word:
          sock.sendall(pickle.dumps(self.word))
      else:
        self.word = pickle.loads(sock.recv(1024))
        self.players, self.bag = pickle.loads(sock.recv(1024))

        self.process_word()
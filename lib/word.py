class Word:
  def __init__(self, player, start, direction, word):
    self.player = player
    self.start = start
    self.direction = direction
    self.word = word
    self.board = None
    self.range = self.set_range()
    self.already_on_board = []
    self.extra_words = []
    self.is_valid = False

  def set_range(self):
    if self.direction == "r":
      return self.set_range_to_right()
    else:
      return self.set_range_to_down()

  def set_range_to_right(self):
    last = chr((ord(self.start[0]) + len(self.word)))
    if len(self.start) == 2:
      return list(map(lambda x: chr(x) + self.start[1], list(range(ord(self.start[0]), ord(last)))))
    else:
      return list(map(lambda x: chr(x) + self.start[1:], list(range(ord(self.start[0]), ord(last)))))

  def set_range_to_down(self):
    if len(self.start) == 2:
      last = int(self.start[1]) - len(self.word)
      return list(map(lambda x: self.start[0] + str(x), list(range(int(self.start[1]), last, -1))))
    else:
      last = int(self.start[1:]) - len(self.word)
      return list(map(lambda x: self.start[0] + str(x), list(range(int(self.start[1:]), last, -1))))

  def set_already_on_board(self):
    for i, spot in enumerate(self.range):
      if self.board[spot] == self.word[i]:
        self.already_on_board.append(word[i])
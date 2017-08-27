class Word:
  def __init__(self, start, direction, word, board):
    self.start = start
    self.direction = direction
    self.word = word
    self.board = board
    self.range = self.set_range()
    self.aob_list = self.set_aob_list()
    self.extra_words = []
    self.extra_spots = []
    self.invalid_word = None

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

  def set_aob_list(self):
    aob_list = []
    for i, spot in enumerate(self.range):
      if self.board[spot] == self.word[i]:
        aob_list.append(self.word[i])
    return aob_list

  def reset(self):
    self.extra_words = []
    self.extra_spots = []
    self.word = None
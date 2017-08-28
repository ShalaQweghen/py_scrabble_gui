class Word:
  def __init__(self, start, direction, word, board, dic):
    self.start = start
    self.dict = dic
    self.direction = direction
    self.word = word
    self.board = board
    self.range = self._set_range()
    self.aob_list = self._set_aob_list()
    self.extra_words = []
    self.extra_spots = []
    self.invalid_word = None

  def process_extra_words(self):
    check_list = []
    aob_list = self.aob_list.copy()

    for i, square in enumerate(self.range):
      extra_word = [self.word[i]]

      if self.board.board[square] in aob_list and self.board.square_occupied(square, self.direction):
        del aob_list[aob_list.index(self.board.board[square])]
        check_list.append(True)
      elif self.board.square_not_occupied(square, self.direction):
        check_list.append(True)
      else:
        self.extra_words.append(self._set_extra_word(square, extra_word))

        if self.dict.valid_word(self.extra_words[-1]):
          self.extra_spots.append((square, self.word[i]))
          check_list.append(True)
        else:
          self.invalid_word = self.extra_words[-1]
          self.extra_words = []
          self.extra_spots = []
          check_list.append(False)

    return not (False in check_list)

  def reset(self):
    self.extra_words = []
    self.extra_spots = []
    self.word = None

  def _set_range(self):
    if self.direction == "r":
      return self._set_range_to_right()
    else:
      return self._set_range_to_down()

  def _set_range_to_right(self):
    last = chr((ord(self.start[0]) + len(self.word)))
    if len(self.start) == 2:
      return list(map(lambda x: chr(x) + self.start[1], list(range(ord(self.start[0]), ord(last)))))
    else:
      return list(map(lambda x: chr(x) + self.start[1:], list(range(ord(self.start[0]), ord(last)))))

  def _set_range_to_down(self):
    if len(self.start) == 2:
      last = int(self.start[1]) - len(self.word)
      return list(map(lambda x: self.start[0] + str(x), list(range(int(self.start[1]), last, -1))))
    else:
      last = int(self.start[1:]) - len(self.word)
      return list(map(lambda x: self.start[0] + str(x), list(range(int(self.start[1:]), last, -1))))

  def _set_aob_list(self):
    aob_list = []
    for i, spot in enumerate(self.range):
      if self.board.board[spot] == self.word[i]:
        aob_list.append(self.word[i])
    return aob_list

  def _set_up_or_left_extra_word(self, square, extra_word):
    while self.board.occupied(square, self.direction, self.board.up_or_left):
      square = self.board.up_or_left(square, self.direction)
      extra_word.insert(0, self.board.board[square])

  def _set_down_or_right_extra_word(self, square, extra_word):
    while self.board.occupied(square, self.direction, self.board.down_or_right):
      square = self.board.down_or_right(square, self.direction)
      extra_word.append(self.board.board[square])

  def _set_extra_word(self, square, extra_word):
    self._set_up_or_left_extra_word(square, extra_word)
    self._set_down_or_right_extra_word(square, extra_word)
    return "".join(extra_word)


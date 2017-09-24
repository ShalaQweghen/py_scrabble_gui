import re

class Word:
  def __init__(self, start, direction, word, board, dic, aob, chal=False):
    self.start = start
    self.dict = dic
    self.direction = direction
    self.word = word
    self.board = board

    self.points = 0
    self.valid = False
    self.wild_tiles = []
    self.extra_words = []
    self.words = {}
    self.aob_list = aob
    self.chal_mode = chal

    self.range = self._set_range()
    self.letter_points = self._set_letter_points()

  def process_extra_words(self):
    check_list = []
    aob_list = self.aob_list.copy()

    for i, square in enumerate(self.range):
      extra_word = [[self.word[i]], [square]]

      if self.board.board[square] in aob_list and self.board.square_occupied(square, self.direction):
        del aob_list[aob_list.index(self.board.board[square])]
        check_list.append(True)
      elif self.board.square_not_occupied(square, self.direction):
        check_list.append(True)
      else:
        self.extra_words.append(self._set_extra_word(square, extra_word))

        if self.chal_mode or self.dict.valid_word(self.extra_words[-1][0]):
          check_list.append(True)
        else:
          self.invalid_word = self.extra_words[-1][0]
          self.extra_words = []
          check_list.append(False)

    return not (False in check_list)

  def calculate_total_points(self):
    if not self.range:
      self.points = 0
      return self.points

    bonus = self.board.calculate_bonus(self.range)
    self.word_bonus = bonus.get('word', None)
    self.letter_bonus = bonus.get('letter', None)

    self.points = self._calculate_word_points(self.word, self.range)

    for word, w_range in self.extra_words:
      self.points += self._calculate_word_points(word, w_range)

    return self.points

  def valid_move(self):
    if not self.range:
      return False

    for square in self.range:
      if self.aob_list:
        return True
      elif self.board.square_occupied(square, self.direction):
        return True

    if self.start == 'h8':
      return True

    return False

  def validate(self):
    if self.valid:
      return True
    else:
      if not self.valid_move():
        self.error_message = 'Move was illegal...'
        return False

      if not self.chal_mode:
        if not self.dict.valid_word(self.word):
          return False

      if not self.process_extra_words():
        return False

      self.valid = True

      return True

  def _set_range(self):
    if self.direction == "r":
      squares = self._set_range_to_right()
    else:
      squares = self._set_range_to_down()

    for s in squares:
      if not re.fullmatch('[a-o]1[0-5]|[a-o][1-9]', s):
        return False

    if not self.board.valid_range(squares, self.word, self.direction):
      return False

    return squares

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

  def _set_up_or_left_extra_word(self, square, extra_word):
    while self.board.occupied(square, self.direction, self.board.up_or_left):
      square = self.board.up_or_left(square, self.direction)
      extra_word[0].insert(0, self.board.board[square])
      extra_word[1].insert(0, square)

  def _set_down_or_right_extra_word(self, square, extra_word):
    while self.board.occupied(square, self.direction, self.board.down_or_right):
      square = self.board.down_or_right(square, self.direction)
      extra_word[0].append(self.board.board[square])
      extra_word[1].append(square)

  def _set_extra_word(self, square, extra_word):
    self._set_up_or_left_extra_word(square, extra_word)
    self._set_down_or_right_extra_word(square, extra_word)
    extra_word[0] = ''.join(extra_word[0])
    return extra_word

  def _set_letter_points(self):
    points = {}
    for letter in list('LSUNRTOAIE'):
      points[letter] = 1
    for letter in list('GD'):
      points[letter] = 2
    for letter in list('BCMP'):
      points[letter] = 3
    for letter in list('FHVWY'):
      points[letter] = 4
    for letter in list('JX'):
      points[letter] = 8
    for letter in list('QZ'):
      points[letter] = 10
    points['K'] = 5
    points['@'] = 0

    return points

  def _calculate_word_points(self, word, w_range):
    word_points = 0

    for l, s in zip(word, w_range):
      if s in self.wild_tiles:
        continue
      elif s in self.board.wild_tiles_on_board:
        continue
      else:
        if self.letter_bonus:
          word_points += self.letter_bonus.get(s, 1) * self.letter_points[l]
        else:
          word_points += self.letter_points[l]

    if self.word_bonus:
      for s in w_range:
        if s != 'h8' or not self.aob_list:
          word_points *= self.word_bonus.get(s, 1)

    self.words[word] = word_points

    return word_points
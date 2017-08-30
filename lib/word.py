import re

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
    self.invalid_word = False
    self.letter_points = self._set_letter_points()
    self.points = self.calculate_points()

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

  def calculate_points(self):
    if not self.range:
      return 0

    bonus = self.board.calculate_bonus(self.range)
    word_bonus = bonus.get('word', None)
    letter_bonus = bonus.get('letter', None)

    word_points = 0
    points = 0

    for l, s in zip(self.word, self.range):
      if letter_bonus:
        word_points += (letter_bonus.get(s, 0) + 1) * self.letter_points[l]
      else:
        word_points += self.letter_points[l]

    if word_bonus:
      for s in self.range:
        points += word_bonus.get(s, 0) * word_points
    else:
      points += word_points

    for w in self.extra_words:
      word_points = 0
      for l in w:
        word_points += self.letter_points[l]
      points += word_points

    for s, l in self.extra_spots:
      if letter_bonus:
        points += letter_bonus.get(s, 0) * self.letter_points[l]

    return points

  def reset(self):
    self.extra_words = []
    self.extra_spots = []
    self.word = None

  def valid_move(self):
    if not self.range:
      return False

    for square in self.range:
      if self.aob_list:
        print(square, 2)
        return True
      elif self.board.square_occupied(square, self.direction):
        return True

    if self.start == 'h8':
      return True

    return False

  def valid(self):
    if not self.valid_move():
      self.error_message = 'Move was illegal...'
      return False

    if not self.dict.valid_word(self.word):
      self.error_message = '{} is not in dictionary...'.format(self.word)
      self.invalid_word = True
      return False

    if not self.process_extra_words():
      self.error_message = '{} is not in the dictionary...'.format(self.invalid_word)
      self.invalid_word = True
      return False

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

  def _set_aob_list(self):
    aob_list = []
    if self.range:
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
# Copyright (C) 2017  Serafettin Yilmaz
#
# See 'py_scrabble.pyw' for more info on copyright

import re

class Word:
  def __init__(self, start, direction, word, board, dic, aob=[], chal=False):
    self.dict = dic
    self.word = word
    self.start = start
    self.board = board
    self.aob_list = aob
    self.chal_mode = chal
    self.direction = direction

    self.points = 0
    self.words = {} # Necessary for showing each word and its points
    self.new = True
    self.valid = False
    self.extra_words = []
    self.wild_letters = []

    self.range = self._set_range()
    self.letter_points = self._set_letter_points()

  # Builds the extra words made by making a word. Populates the extra words
  # array and return True if all the words are valid.
  def process_extra_words(self):
    check_list = []
    aob_list = self.aob_list.copy()

    # There can be extra words as many as the spots in the word range are
    for letter_index, square in enumerate(self.range):
      # The array in 0 index is the array for the word
      # the one in 1 index is for bonuses if any
      extra_word = [[self.word[letter_index]], [square]]

      # If the letter is already on the board and there are occupied spot around it,
      # It means it can't make extra words but it is already valid
      if self.board.board[square] in aob_list and self.board.square_occupied(square, self.direction):
        del aob_list[aob_list.index(self.board.board[square])]
        check_list.append(True)
      # If it is not already on the board and there are no occupied squares
      # It is a valid one because it is standing alone not in an extra word
      elif self.board.square_not_occupied(square, self.direction):
        check_list.append(True)
      # If the letter is not already on the board and there are spots occupied
      # around it, it means it is suitable to make an extra word
      else:
        self.extra_words.append(self._set_extra_word(square, extra_word))

        # In challenge mode, no need to check if it is in the dictionary
        # Check the last word as others are already checked
        if self.chal_mode or self.dict.valid_word(self.extra_words[-1][0]):
          check_list.append(True)
        else:
          # Record the invalid word and reset the extra words
          self.invalid_word = self.extra_words[-1][0]
          self.extra_words = []
          check_list.append(False)

    return not (False in check_list)

  def calculate_total_points(self):
    # This one is important for computer words
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

    # For a word to be valid, either it should make use of an already
    # on board letter or one of its letters should be connected to
    # a word already on the board
    for square in self.range:
      if self.aob_list:
        return True
      elif self.board.square_occupied(square, self.direction):
        return True

    # If it is not connected to any words, it might mean it is the
    # first turn. In that case, it should start from 'h8', that is,
    # from the middle square.
    if self.start == 'h8':
      return True

    return False

  def validate(self):
    # No need to evaluate it twice
    if self.valid:
      return True
    else:
      if not self.valid_move():
        return False

      if not self.chal_mode:
        if not self.dict.valid_word(self.word):
          return False

      if not self.process_extra_words():
        return False

      # Not to process the word twice accidentally
      self.new = False
      self.valid = True

      return True

  # Return range if valid or False
  def _set_range(self):
    if self.direction == "r":
      squares = self._set_range_to_right()
    else:
      squares = self._set_range_to_down()

    # Check if the squares returned are in the range of 'a' to 'o' and 1 to 15
    for s in squares:
      if not re.fullmatch('[a-o]1[0-5]|[a-o][1-9]', s):
        return False

    if not self.board.valid_range(squares, self.word, self.direction):
      return False

    return squares

  def _set_range_to_right(self):
    # Determine the letter part of the last square of the word.
    # Because it is to the right, modify the letter part
    last = chr((ord(self.start[0]) + len(self.word)))

    # Check if the number part is 1 digit or 2 digits
    if len(self.start) == 2:
      # Make a list of letters by making use of ascii numbers
      letter_range = list(range(ord(self.start[0]), ord(last)))

      # Map the number part of the spot with letters in the range
      return list(map(lambda x: chr(x) + self.start[1], letter_range))
    else:
      letter_range = list(range(ord(self.start[0]), ord(last)))

      return list(map(lambda x: chr(x) + self.start[1:], letter_range))

  def _set_range_to_down(self):
    # Check if the number part is 1 digit or 2 digits
    if len(self.start) == 2:
      # Determine the number part of the last square of the word.
      # Because it is to the down, modify the number part.
      # Numbers decrease as it goes down. This one is 1 digit.
      last = int(self.start[1]) - len(self.word)
      # Make a list of numbers in reverse order
      number_range = list(range(int(self.start[1]), last, -1))

      # Map the letter part of the spot with numbers in the range
      return list(map(lambda x: self.start[0] + str(x), number_range))
    else:
      last = int(self.start[1:]) - len(self.word)
      number_range = list(range(int(self.start[1:]), last, -1))

      return list(map(lambda x: self.start[0] + str(x), number_range))

  def _set_up_or_left_extra_word(self, square, extra_word):
    while self.board.occupied(square, self.direction, self.board.up_or_left):
      square = self.board.up_or_left(square, self.direction)
      # If the occupied squares are towards right or up,
      # the letters should be added to the beginning of the array
      extra_word[0].insert(0, self.board.board[square])
      extra_word[1].insert(0, square)

  def _set_down_or_right_extra_word(self, square, extra_word):
    while self.board.occupied(square, self.direction, self.board.down_or_right):
      square = self.board.down_or_right(square, self.direction)
      # If the occupied squares are towards left or down,
      # the letters should be added to the end of the array
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

    for letter, square in zip(word, w_range):
      # If the letter is a wild letter, no points
      if square in self.wild_letters:
        continue
      elif square in self.board.wild_letters_on_board:
        continue
      else:
        if self.letter_bonus:
          word_points += self.letter_bonus.get(square, 1) * self.letter_points[letter]
        else:
          word_points += self.letter_points[letter]

    if self.word_bonus:
      for square in w_range:
        # Avoid using h8 bonus twice
        if square != 'h8' or not self.aob_list:
          word_points *= self.word_bonus.get(square, 1)

    self.words[word] = word_points

    return word_points
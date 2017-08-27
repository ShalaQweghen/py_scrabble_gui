def set_up_or_left_extra_word(square, word, extra_word):
  while square_occupied_up_or_left(square, word):
    square = up_or_left(square, word.direction)
    extra_word.insert(0, word.board[square])

def set_down_or_right_extra_word(square, word, extra_word):
  while square_occupied_down_or_right(square, word):
    square = down_or_right(square, word.direction)
    extra_word.append(word.board[square])

def set_extra_word(square, word, extra_word):
  set_up_or_left_extra_word(square, word, extra_word)
  set_down_or_right_extra_word(square, word, extra_word)
  return "".join(extra_word)

def process_extra_words(word, dic):
  check_list = []
  aob_list = word.aob_list.copy()

  for i, square in enumerate(word.range):
    extra_word = [word.word[i]]

    if word.board[square] in aob_list and square_occupied(square, word):
      del aob_list[aob_list.index(word.board[square])]
      check_list.append(True)
    elif not square_occupied_up_or_left(square, word) and not square_occupied_down_or_right(square, word):
      check_list.append(True)
    else:
      word.extra_words.append(set_extra_word(square, word, extra_word))

      if dic.valid_word(word.extra_words[-1]):
        word.extra_spots.append((square, word.word[i]))
        check_list.append(True)
      else:
        word.extra_words = []
        word.extra_spots = []
        check_list.append(False)

  return not (False in check_list)

def up_move(square):
  if len(square) == 2:
    return square[0] + str(int(square[1]) + 1)
  else:
    return square[0] + str(int(square[1:]) + 1)

def down_move(square):
  if len(square) == 2:
    return square[0] + str(int(square[1]) - 1)
  else:
    return square[0] + str(int(square[1:]) - 1)

def left_move(square):
  if len(square) == 2:
    return chr(ord(square[0]) - 1) + square[1]
  else:
    return chr(ord(square[0]) - 1) + square[1:]

def right_move(square):
  if len(square) == 2:
    return chr(ord(square[0]) + 1) + square[1]
  else:
    return chr(ord(square[0]) + 1) + square[1:]

def up_or_left(square, direction):
  if direction == 'r':
    return up_move(square)
  else:
    return left_move(square)

def down_or_right(square, direction):
  if direction == 'r':
    return down_move(square)
  else:
    return right_move(square)

def square_occupied_up_or_left(square, word):
  return ord(word.board.get(up_or_left(square, word.direction), ['.'])[0]) in range(65, 91)

def square_occupied_down_or_right(square, word):
  return ord(word.board.get(down_or_right(square, word.direction), ['.'])[0]) in range(65, 91)

def square_occupied(square, word):
  return square_occupied_down_or_right(square, word) or square_occupied_up_or_left(square, word)

def set_letter_points():
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
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

def occupied_up_or_left(direction, square, board):
  return ord(board.board.get(up_or_left(square, direction), ['.'])[0]) in range(65, 91)


def occupied_down_or_right(direction, square, board):
  return ord(board.board.get(down_or_right(square, direction), ['.'])[0]) in range(65, 91)
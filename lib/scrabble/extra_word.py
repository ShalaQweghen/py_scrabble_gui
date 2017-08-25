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

def left_move(square):
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

def occupied_up_or_left(square, board):
	return ord(board[up_or_left]) in range(65, 91)

def occupied_down_or_right(square, board):
	return ord(board[down_or_right]) in range(65, 91)

def set_up_or_left_extra_word(square, direction, board, eword, eset):
	while occupied_up_or_left(square, board):
		square = up_or_left(square, direction)
		eword.insert(0, board[square])
		eset.insert(square)

def set_down_or_right_extra_word(square, direction, board, eword, eset):
	while occupied_down_or_right(square, board):
		square = up_or_left(square, direction)
		eword.append(board[square])
		eset.append(square)

def set_extra_word(square, eset, eword, wlist, word, wset, board, direction):
	eset = [].append(square)
	eword = [].append(word[wset.index(square)])
	set_up_or_left_extra_word(sqaure, direction, board, eword, eset)
	set_down_or_right_extra_word(sqaure, direction, board, eword, eset)
	wlist.append("".join(eword))

def extra_word(square, nlist, board, eset, eword, wlist, score, direction, dic):
	nlist_clone = nlist.copy()
	if board[square] in nlist_clone and (occupied_up_or_left(square, board) or occupied_down_or_right(square, board)):
		del nlist_clone(nlist_clone.index(board[square]))
		return True
	else if not occupied_up_or_left(square, board) and not occupied_down_or_right(square, board):
		return True
	else:
		set_extra_word(square, eset, eword, wlist, word, wset, board, direction)
		if "".join(eword) in dic:
			score += calculate_points("".join(eword), eset)
			return True
		else:
			return False
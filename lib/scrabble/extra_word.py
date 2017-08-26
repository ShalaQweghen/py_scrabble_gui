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
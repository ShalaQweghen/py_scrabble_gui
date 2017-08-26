from .valid_move_helpers import *

def set_up_or_left_extra_word(square, word, extra_word):
	while occupied_up_or_left(square, word):
		square = up_or_left(square, word.direction)
		extra_word.insert(0, word.board[square])

def set_down_or_right_extra_word(square, word, extra_word):
	while occupied_down_or_right(square, word):
		square = down_or_right(square, word.direction)
		extra_word.append(word.board[square])

def set_extra_word(square, word, extra_word):
	set_up_or_left_extra_word(square, word, extra_word)
	set_down_or_right_extra_word(square, word, extra_word)
	return "".join(extra_word)

def check_extra_word(word, word_list, dic):
	check_list = []
	not_discard_list_clone = word.already_on_board.copy()

	for i, square in enumerate(word.range):
		extra_word = [word.word[i]]

		if word.board[square] in not_discard_list_clone and (occupied_up_or_left(square, word) or occupied_down_or_right(square, word)):
			del not_discard_list_clone[not_discard_list_clone.index(word.board[square])]
			check_list.append(True)
		elif not occupied_up_or_left(square, word) and not occupied_down_or_right(square, word):
			check_list.append(True)
		else:
			word_list.append(set_extra_word(square, word, extra_word))

			if dic.valid_word(word_list[-1]):
				check_list.append(True)
			else:
				word_list = []
				check_list.append(False)

	return not (False in check_list)
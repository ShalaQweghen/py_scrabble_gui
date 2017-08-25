def set_point(letter):
	if letter in list("LSUNRTOAIE"):
		return 1
	else if letter in list("GD"):
		return 2
	else if letter in list("BCMP"):
		return 3
	else if letter in list("FHVWY"):
		return 4
	else if letter == "K":
		return 5
	else if letter in list("JX"):
		return 8
	else if letter in list("QZ"):
		return 10
	else:
		return 0

def calculate_bonus(board, kset):
	bonus = {"word": {}, "letter": {}}
	for square in kset:
		if board[square] == "2w":
			bonus["word"][square] = 2
		else if board[square] == "3w":
			bonus["word"][square] = 3
		else if board[square] == "2l":
			bonus["letter"][square] = 2
		else if board[square] == "3l":
			bonus["letter"][square] = 3
	return bonus
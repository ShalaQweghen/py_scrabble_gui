
def set_word_range(player):
	if player.direction == "r":
		wset = set_word_range_to_right(player)
	else:
		wset = set_word_range_to_down(player)
	return wset

def set_word_range_to_right(player):
	last = chr((ord(player.start[0]) + len(player.word)))
	if len(player.start) == 2:
		kset = list(map(lambda x: chr(x) + player.start[1], list(range(ord(player.start[0]), ord(last)))))
	else:
		kset = list(map(lambda x: chr(x) + player.start[1:], list(range(ord(player.start[0]), ord(last)))))
	return kset

def set_word_range_to_down(player):
	if len(player.start) == 2:
		last = int(player.start[1]) - len(player.word) + 1
		kset = list(map(lambda x: player.start[0] + str(x), list(range(last, int(player.start[1]) + 1))))
	else:
		last = int(player.start[1:]) - len(player.word) + 1
		kset = list(map(lambda x: player.start[0] + str(x), list(range(last, int(player.start[1:]) + 1))))
	return kset

def set_non_discard(kset, nlist, board, word):
	for i, key in enumerate(wset):
		if board[key] == word[i]:
			nlist.append(word[i])

def letters_on_rack(player, nlist, wtile):
	for l in list(player.word):
		if not l in player.letters or not l == wtile or not l in nlist:
			return False
	return True

def discard_used_letters(player, nlist, wtile):
	if letters_on_rack():
		for l in list(player.word):
			if not l in nlist:
				if wtile and wtile == l:
					l = '@'
					wtile = None
				del player.letters[player.letters.index(l)]
			else:
				del nlist[nlist.index(l)]
	else:
		raise TypeError

def place_word(wset, nlist, board, player, wlist):
	for i, key in enumerate(wset):
		if not player.word[i] in nlist:
			board[key] = player.word[i]
	wlist.append(player.word)

def change_letters(player, bag):
	for l in player.passed:
		bag.append(player.letters[player.letters.index(l)])
		del player.letters[player.letters.index(l)]

def ask_wild_tile(player):
	player.output.write("What letter would you like to replace with the wild tile?:")
	return player.input.readline()[:-1].upper()

def set_wild_tile(player):
	if "@" in player.word:
		wtile = ask_wild_tile(player)
		player.word[player.word.index("@")] = wtile

def process_word(player, kset, nlist, board):
	set_word_range(player)
	set_wild_tile(player)
	set_non_discard(kset, nlist, board, player.word)

def reset_word_list(w, wlist, pwlist):
	w.extend(wlist)
	pwlist = wlist.copy()
	wlist = []
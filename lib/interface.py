import sys

from game import Game

class Interface:
	def __init__(self):
		print('COMMANDLINE SCRABBLE'.center(50))
		self.give_main_options()

	def give_main_options(self):
		print('\n0 => README')
		print('1 => Game options on this computer')
		print('2 => Game options on the network')
		print('9 => Exit')

		action = input('\nPick an action: ')

		if action == '0': pass
		elif action == '1': self.start_local_game()
		elif action == '2': pass
		elif action == '9': sys.exit()
		else: self.give_main_options()

	def start_local_game(self):
		options = self.give_secondary_options()
		Game(options).enter_game_loop()

	def give_secondary_options(self):
		print('\n1 => Start a new game on normal mode')
		print('2 => Start a new game on challenge mode')
		print('3 => Start a new game on normal mode with a time limit')
		print('4 => Start a new game on challenge mode with a time limit')
		print('5 => Continue a saved game')
		print('9 => Go to previous menu')
		print('0 => Exit')

		action = input('\nPick an action: ')

		if action == '1': return {}
		elif action == '2': return {'challenge': True}
		elif action == '3': return {'limit': input('\nPlease enter the time limit in minutes: ')}
		elif action == '4': return {'challenge': True, 'limit': input('\nPlease enter the time limit in minutes: ')}
		elif action == '5': return {'saved': True}
		elif action == '9': self.give_main_options()
		elif action == '0': sys.exit()
		else: self.give_secondary_options()

Interface()
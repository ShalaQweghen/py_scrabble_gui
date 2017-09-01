import sys, socket

from lib.game import Game

class Interface:
	def __init__(self, config):
		self.options = config

		print()
		print('\033[1mCOMMANDLINE SCRABBLE\033[0m'.center(50))

		self.give_main_options()

	def give_main_options(self):
		print('\n\033[1m0\033[0m => README')
		print('\033[1m1\033[0m => Game against computer')
		print('\033[1m2\033[0m => Game options on this computer')
		print('\033[1m3\033[0m => Game options on the network')
		print('\n\033[1m9\033[0m => Exit')

		action = input('\nPick an action: ')

		if action 	== '0': self.print_read_me()
		elif action == '1': self.start_against_comp()
		elif action == '2': self.start_local_game()
		elif action == '3': self.start_network_game()
		elif action == '9': sys.exit()
		else: self.give_main_options()

	def print_read_me(self):
		readme = open('./lib/README.txt', 'r').read()
		print(readme)
		self.give_main_options()

	def start_against_comp(self):
		self.options.update(self.give_secondary_options(computer=True))
		self.options['comp_game'] = True

		Game(self.options).enter_game_loop()

	def start_local_game(self):
		self.options.update(self.give_secondary_options())

		if not self.options.get('load_game', False):
			self.options['players'] = input('\nHow many players will there be (2, 3, or 4)? ').strip()

			while self.options['players'] not in ['2', '3', '4']:
				self.options['players'] = input('\n2, 3, or 4: ')

		Game(self.options).enter_game_loop()

	def start_network_game(self):
		self.options.update(self.give_secondary_options(False))
		self.options['players'] = input('\nHow many players will there be (2, 3, or 4)? ').strip()

		while self.options['players'] not in ['2', '3', '4']:
			self.options['players'] = input('\n2, 3, or 4: ')

		sock = socket.socket()
		sock.setblocking(True)
		host = '192.168.1.7'
		port = 12345

		sock.bind((host, port))

		sock.listen()
		print('\nServer fired up on {}:{}... Waiting for opponents...\n'.format(host, port))

		self.options['streams'] = []

		for i in range(int(self.options['players']) - 1):
			cli, addr = sock.accept()

			c_input = cli.makefile('r')
			c_output = cli.makefile('w')

			self.options['streams'].append((c_input, c_output))

		self.options['network_game'] = True

		Game(self.options).enter_game_loop()


	def give_secondary_options(self, continuable=True, computer=False):
		print('\n\033[1m1\033[0m => Start a new game on normal mode')
		print('\033[1m2\033[0m => Start a new game on challenge mode')

		if not computer:
			print('\033[1m3\033[0m => Start a new game on normal mode with a time limit')
			print('\033[1m4\033[0m => Start a new game on challenge mode with a time limit')
		else:
			print()

		if continuable:
			print('\033[1m5\033[0m => Continue a saved game\n')
		else:
			print()

		print('\033[1m9\033[0m => Go to previous menu')
		print('\033[1m0\033[0m => Exit')

		action = input('\nPick an action: ')

		if action == '1': return {}
		elif action == '2': return {'challenge': True}
		elif not computer and action == '3': return {'time_limit': input('\nPlease enter the time limit in minutes: ')}
		elif not computer and action == '4': return {'challenge_mode': True, 'time_limit': input('\nPlease enter the time limit in minutes: ')}
		elif continuable and action == '5': return {'load_game': True}
		elif action == '9': self.give_main_options()
		elif action == '0': sys.exit()
		else: self.give_secondary_options(continuable, computer)
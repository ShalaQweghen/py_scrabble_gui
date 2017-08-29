import sys, socket

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

		if action 	== '0': self.print_read_me()
		elif action == '1': self.start_local_game()
		elif action == '2': self.start_network_game()
		elif action == '9': sys.exit()
		else: self.give_main_options()

	def print_read_me(self):
		readme = open('./lib/README.txt', 'r').read()
		print(readme)
		self.give_main_options()

	def start_local_game(self):
		options = self.give_secondary_options()
		options['players'] = int(input('\nHow many players will there be (2, 3, or 4)? '))

		while options['players'] not in [2, 3, 4]:
			options['players'] = int(input('\n2, 3, or 4: '))

		Game(options).enter_game_loop()

	def start_network_game(self):
		options = self.give_secondary_options()
		options['players'] = int(input('\nHow many players will there be (2, 3, or 4)? '))

		while options['players'] not in [2, 3, 4]:
			options['players'] = int(input('\n2, 3, or 4: '))

		sock = socket.socket()
		sock.setblocking(True)
		host = '192.168.1.7'
		port = 12345

		sock.bind((host, port))

		sock.listen()
		print('\nServer fired up on {}:{}... Waiting for opponents...\n'.format(host, port))

		options['streams'] = []

		for i in range(options['players'] - 1):
			cli, addr = sock.accept()

			c_input = cli.makefile('r')
			c_output = cli.makefile('w')

			options['streams'].append((c_input, c_output))

		options['network'] = True

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
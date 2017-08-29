import pickle, os, sys, subprocess

from player import Player

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

def save(game):
  if not os.path.exists('./saves'):
    os.mkdir('./saves')

  filename = ask_filename(game)

  while os.path.exists('./saves/' + filename + '.obj'):
    game.current_player.output.write('\n' + filename +  ' already exists.\n')
    filename = ask_filename(game)

  players_list = []

  for p in game.players_list:
    players_list.append([p.name, p.score, p.letters])

  data = {}
  data['board'] = game.board
  data['bag'] = game.bag
  data['turns'] = game.turns - 1
  data['passes'] = game.passes
  data['points'] = game.points
  data['words'] = game.words
  data['word'] = game.word
  data['limit'] = game.limit
  data['challenging'] = game.challenging
  data['players'] = game.players
  data['players_info'] = players_list

  file = open('./saves/' + filename + '.obj', 'wb')
  pickle.dump(data, file)

def load(game):
  if not os.path.exists('./saves'):
    print('\nThere are no save files. Starting a new game...')
    start_anew(game)

  file_list = subprocess.check_output('ls saves | grep obj', shell=True)

  print('\nFiles in the saves folder:\n')
  print(file_list[:-1].decode('utf-8'))

  filename = input('\nWhat is the name of your file without .obj? ')

  if not os.path.exists('./saves/' + filename + '.obj'):
    print('\nNo such file. Starting a new game...')
    start_anew(game)

  file = open('./saves/' + filename + '.obj', 'rb')
  data = pickle.load(file)

  game.board = data['board']
  game.bag = data['bag']
  game.turns = data['turns']
  game.passes = data['passes']
  game.points = data['points']
  game.words = data['words']
  game.word = data['word']
  game.limit = data['limit']
  game.challenging = data['challenging']
  game.players = data['players']

  for p in data['players_info']:
    player = Player(name=p[0])
    player.score = p[1]
    player.letters = p[2]
    game.players_list.append(player)

def ask_filename(game):
  game.current_player.output.write('\nGive a name to the save file: ')
  filename = game.current_player.input.readline()[:-1]
  return filename

def start_anew(game):
  os.system('sleep 1')
  game.saved = False
  game.enter_game_loop()
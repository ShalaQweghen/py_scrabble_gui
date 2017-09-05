import random, time, sys

import lib.helpers as helpers

from lib.bag import Bag
from lib.board import Board
from lib.player import Player
from lib.dic import Dict
from lib.comp import AIOpponent

class Game:
  def __init__(self, config={}):
    self.board = Board()
    self.bag = Bag()
    self.dict = Dict('./dics/sowpods.txt')
    self.turns = 0
    self.passes = 0
    self.points = 0
    self.words = []
    self.word = None
    self.human = None
    self.words_list = set()
    self.players_list = []

    self.streams = config.get('streams', False)
    self.players = int(config.get('players', 2))
    self.time_limit = config.get('time_limit', False)
    self.save_meaning = config.get('save_meaning', False)

    self.comp_game = config.get('comp_game', False)
    self.load_game = config.get('load_game', False)
    self.network_game = config.get('network_game', False)

    self.challenge_mode = config.get('challenge_mode', False)

  def initialize_game(self):
    if self.load_game:
      helpers.load(self)
      self.current_player = self.players_list[self.turns % self.players]
    elif self.comp_game:
      self.human = Player()
      self.players_list.extend([AIOpponent(), self.human])
      self.players_list[0].name = 'COMP'
      self.players_list[-1].name = input('\nWhat is your name?: ').upper()

      for p in self.players_list:
        p.draw_letters(self.bag)

      random.shuffle(self.players_list)
      self.current_player = self.players_list[0]
      self.prev_player = self.current_player.name
    else:
      for p in range(self.players):
        if self.streams:
          player = Player(self.streams[p][0], self.streams[p][1])
          if p == len(self.streams) - 1:
            self.streams = False
        else:
          player = Player()

        player.output.write('\nWhat is Player {}\'s name?: \n'.format(p + 1))
        player.output.flush()
        player.name = player.input.readline()[:-1].upper()
        player.draw_letters(self.bag)

        self.players_list.append(player)

      if self.time_limit:
        self.set_time_limit()

      random.shuffle(self.players_list)
      self.current_player = self.players_list[0]
      self.prev_player = self.current_player.name

  def initialize_turn(self):
    if self.word:
      self.words.append(self.word.word)
      self.words.extend(list(map(lambda x: x[0], self.word.extra_words)))
      self.words_list = self.words_list.union(set(self.words))

    self.prev_player = self.current_player

    if self.network_game:
      for p in self.players_list:
        self.board.display(p.output)
        self.display_turn_info(p)

      self.current_player = self.players_list[self.turns % self.players]

      for p in self.players_list:
        if p is not self.current_player:
          p.output.write("\nIt's {}'s turn... {}\n\n".format(self.current_player.name, self.current_player))
          p.output.flush()
    else:
      self.current_player = self.players_list[self.turns % self.players]

      if self.current_player is self.human or not self.comp_game:
        self.board.display(self.current_player.output)
        self.display_turn_info(self.current_player)
      elif self.comp_game:
        self.board.display(self.human.output)
        self.display_turn_info(self.human)
        print('\nIt\'s Computer\'s turn... {}\n'.format(self.current_player))

    self.turns += 1
    self.words = []

  def display_turn_info(self, p):
    p.output.write(
      "\n\033[1mPlayer:\033[0m {}\t\t\033[1m|\033[0m  \033[1mTotal Points:\033[0m {}\n".format(
        p.name, p.score
      )
    )
    p.output.write(
      "\033[1mLetters Left in Bag:\033[0m {}\t\033[1m|\033[0m  \033[1mWords:\033[0m {} for {} pts by {}\n\n".format(
        len(self.bag.bag), self.words, self.points, self.prev_player.name
      )
    )
    p.output.write("\u2551 {} \u2551\n".format(' - '.join(p.letters)).center(70))
    p.output.flush()

  def play_turn(self):
    self.current_player.get_move(self.bag, self.board, self.dict)

    while self.current_player.is_saving:
      helpers.save(self)
      self.current_player.get_move(self.bag, self.board, self.dict)

    self.word = self.current_player.word

    if self.current_player.is_passing:
      self.passes += 1
      self.word = None
      self.words = []
      self.points = 0
    elif self.move_acceptable() and self.word.validate():
      if self.word.wild_tiles:
        self.board.wild_tiles_on_board.extend(self.word.wild_tiles)

      self.points = self.word.calculate_total_points()

      if self.turns == 1:
        self.points *= 2

      self.board.place(self.word.word, self.word.range)
      self.current_player.update_rack(self.bag)

      if self.current_player.full_bonus and len(self.bag.bag) > 0:
        self.points += 60

      self.current_player.update_score(self.points)
      self.passes = 0
    else:
        self.current_player.display_message(self.word.error_message)
        if self.word.invalid_word:
          self.handle_invalid_word()
        else:
          self.play_turn()

  def racks_not_empty(self):
    for p in self.players_list:
      if len(p.letters) == 0:
        return False

    return True

  def move_acceptable(self):
    if self.time_limit and self.time_over():
      self.end_game()
      return False

    return True

  def handle_invalid_word(self):
    self.current_player.return_wild_tile()

    if not self.challenge_mode:
      self.play_turn()
    else:
      self.passes += 1
      self.points = 0
      self.word.reset()

  def set_time_limit(self):
    try:
      start_time = time.time()
      self.end_time = start_time + int(self.time_limit) * 60
    except ValueError:
      print('\nTime limit should be a whole number (1, 2, etc)...')
      self.time_limit = input('Please enter the time limit in minutes: ')
      self.set_time_limit()

  def time_over(self):
    return time.time() >= self.end_time

  def decide_winner(self):
    winner = self.current_player

    for p in self.players_list:
      if p.score > winner.score:
        winner = p

    return winner

  def display_last_turn_info(self, output):
    self.words.append(self.word.word)
    self.words.extend(list(map(lambda x: x[0], self.word.extra_words)))
    self.words_list = self.words_list.union(set(self.words))
    self.board.display(output)

    output.write('\n\n')
    output.write("\033[1mWords:\033[0m {} for {} pts by {}\n\n".format(self.words, self.points, self.current_player.name).center(75))
    output.flush()

  def end_game(self):
    self.remove_points()

    winner = self.decide_winner()

    for p in ((self.network_game and self.players_list) or [self.current_player]):
      if self.time_limit and self.time_over():
        p.output.write('\n==================================================================\n\n')
        p.output.write('TIME IS UP!\n'.center(70))
      else:
        self.display_last_turn_info(p.output)

        p.output.write('\n==================================================================\n\n')
        p.output.write('GAME IS OVER!\n'.center(70))

      p.output.write('\n')

      for pl in self.players_list:
        p.output.write((str(pl) + '\n').center(70))

      p.output.write('\n')

      p.output.write('The winner is \033[1m{}\033[0m with \033[1m{}\033[0m points!\n'.format(winner.name, winner.score).center(85))
      p.output.write('\n==================================================================\n')

    if self.save_meaning:
      helpers.get_meaning(self.words_list)

    sys.exit()

  def remove_points(self):
    for p in self.players_list:
      while p.letters:
        for l in p.letters:
          p.update_score(-(self.prev_player.word.letter_points[l]))
          p.letters.remove(l)

  def enter_game_loop(self):
    try:
      self.initialize_game()
      while self.racks_not_empty() and self.passes != 3 * self.players:
        try:
          self.initialize_turn()
          self.play_turn()
        except KeyboardInterrupt:
          answer = input('\nAre you sure about cancelling the game (y/n) ?: ').upper().strip()
          if answer.startswith('Y'):
            sys.exit()
          else:
            self.turns -= 1
      self.end_game()
    except (BrokenPipeError, ConnectionResetError):
        for p in self.players_list:
          try:
            p.output.write('\nA player has quit the game. The game is cancelled.\n\n')
            p.output.flush()
          except:
            continue

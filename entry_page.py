import pickle, os

from tkinter import *
from tkinter.filedialog import askopenfilename

from game_page import GamePage
from start_page import NormalStartPage#, LANStartPage

class EntryPage(Frame):
  def __init__(self, parent, dic='./dics/sowpods.txt'):
    self.parent = parent
    self.dict = dic

    Frame.__init__(self, parent, bg='azure')
    self.grid(row=0, column=0, sticky=S+N+E+W)

    self.parent.master.geometry("704x420")
    self.draw()

  def draw(self):
    Label(self, text='Welcome to PyScrabble', font=('times', 40, 'italic'), bg='azure', pady=100).pack(side=TOP)

    f = Frame(self, bg='azure')
    f.pack(side=TOP)

    Button(f, text='Start Computer Game', command=self.start_computer_game).pack(side=LEFT, padx=10)
    Button(f, text='Start Game on Computer', command=self.start_normal_game).pack(side=LEFT, padx=10)
    Button(f, text='Start Game on LAN', command=lambda: self.go_to_frame('LANStartPage')).pack(side=LEFT, padx=10)

    Button(self, text='Load Game', command=self.load_game).pack(side=TOP, pady=30)


  def start_computer_game(self):
    self.parent.master.geometry("750x785")
    self.parent.master.minsize(750, 785)

    page = GamePage(self.parent, {'comp_mode': True, 'names': ['Player', 'Computer'], 'players': 2}, self.dict)
    page.tkraise()

  def start_normal_game(self):
    self.parent.master.geometry("704x440")
    self.parent.master.minsize(704, 440)

    page = NormalStartPage(self.parent, self.dict)
    page.tkraise()

  def load_game(self):
    filename = askopenfilename(initialdir='./saves', filetypes=(('Pickle Files', '*.pickle'),))

    if filename:
      file = open(filename, 'rb')
      data = pickle.load(file)

      options = {
                  'challenge_mode': data['chal_mode'],
                  'comp_mode': data['comp_mode'],
                  'normal_mode': data['norm_mode'],
                  'time_limit': data['time_limit'],
                  'point_limit': data['point_limit'],
                  'names': data['players'],
                  'players': data['play_num'],
                  'loading': True
                }

      self.parent.master.geometry("750x785")
      self.parent.master.minsize(750, 785)

      game = GamePage(self.master, options)

      game.player_racks = data['player_racks']
      game.player_scores = data['player_scores']
      game.cur_play_mark = data['cur_play_mark']
      game.bag = data['bag']
      game.board = data['board']
      game.op_score = data['op_score']
      game.seconds = data['seconds']
      game.minutes = data['minutes']




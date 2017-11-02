# Copyright (C) 2017  Serafettin Yilmaz
#
# See 'py_scrabble.pyw' for more info on copyright

import pickle, re

from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.simpledialog import askstring
from tkinter.messagebox import showwarning

from lib.gui.game_page import GamePage
from lib.gui.start_page import NormalStartPage, LANStartPage

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
    Button(f, text='Start Game on LAN', command=self.start_lan_game).pack(side=LEFT, padx=10)

    fb = Frame(self, bg='azure')
    fb.pack(side=TOP)

    Button(fb, text='Join a Game (Auto)', command=self.join_game).pack(side=LEFT, pady=20, padx=10)
    Button(fb, text='Join a Game (IP)', command=self.join_with_ip).pack(side=LEFT, pady=20, padx=10)

    Button(self, text='Load Game', command=self.load_game).pack(side=TOP)


  def start_computer_game(self):
    self.parent.master.set_geometry()

    GamePage(self.parent, {'comp_mode': True, 'names': ['Player', 'Computer'], 'play_num': 2}, self.dict)

  def start_normal_game(self):
    self.parent.master.geometry("704x400")
    self.parent.master.minsize(704, 400)

    NormalStartPage(self.parent, self.dict)

  def start_lan_game(self):
    self.parent.master.geometry("704x450")
    self.parent.master.minsize(704, 450)

    LANStartPage(self.parent, self.dict)

  def load_game(self):
    filename = askopenfilename(initialdir='./saves', filetypes=(('Pickle Files', '*.pickle'),))

    if filename:
      file = open(filename, 'rb')
      data = pickle.load(file)

      options = {
                  'chal_mode': data['chal_mode'],
                  'comp_mode': data['comp_mode'],
                  'normal_mode': data['norm_mode'],
                  'time_limit': data['time_limit'],
                  'point_limit': data['point_limit'],
                  'play_num': data['play_num'],
                  'loading': True
                }

      self.parent.master.set_geometry()

      game = GamePage(self.master, options)

      game.cur_play_mark = data['cur_play_mark']
      game.players = data['players']
      game.bag = data['bag']
      game.board = data['board']
      game.op_score = data['op_score']
      game.seconds = data['seconds']
      game.minutes = data['minutes']
      game.turns = data['turns']

  def join_game(self):
    name = askstring('Enter Name', 'Enter your name:')

    if name:
      self.parent.master.set_geometry()
      self.parent.master.child = GamePage(self.parent, {'names': [name]})
    else:
      showwarning('No Name', 'No Name Provided.\n\nTry Again.')

  def join_with_ip(self):
    name = askstring('Enter Name', 'Enter your name:')

    if name:
      ip = askstring('Enter IP Address', 'Enter the Host IP Address:')
      p = '(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])'
      ip_p = p + '\.' + p + '\.' + p + '\.' + p

      if re.fullmatch(ip_p, ip):
        self.parent.master.set_geometry()
        self.parent.master.child = GamePage(self.parent, {'names': [name], 'ip': ip})
      else:
        showwarning('Invalid Entry', 'IP Address is Invalid.\n\nTry Again.')
    else:
      showwarning('No Name', 'No Name Provided.\n\nTry Again.')
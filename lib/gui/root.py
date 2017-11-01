# Copyright (C) 2017  Serafettin Yilmaz
#
# See 'py_scrabble.pyw' for more info on copyright

import sys

from tkinter import *
from tkinter.messagebox import askyesno

from lib.gui.entry_page import EntryPage

class Root(Tk):
  def __init__(self, dic='./dics/sowpods.txt'):
    Tk.__init__(self)
    self.title('PyScrabble')
    self.config(bg='azure')
    self.protocol('WM_DELETE_WINDOW', self.quit_game)

    self.dict = dic

    self.child = None # Necessary for preventing lag in lan games

    # Center the game window
    ws = self.winfo_screenwidth()
    x = int((ws/2) - (704/2))

    self.geometry('704x420+{}+{}'.format(x, 0))
    self.minsize(704, 420)

    self.draw_menu()
    self.draw_container()

    EntryPage(self.container, self.dict)

  def draw_menu(self):
    top = Menu(self)
    self.config(menu=top)

    game_m = Menu(top)
    game_m.add_command(label='New Game', underline=0, command=self.start_new)
    game_m.add_command(label='Quit', underline=0, command=self.quit_game)

    top.add_cascade(label='Game', menu=game_m, underline=0)

  def draw_container(self):
    self.container = Frame(self, bg='azure')
    self.container.pack(side=TOP, fill=BOTH, expand=YES)
    self.container.grid_rowconfigure(0, weight=1)
    self.container.grid_columnconfigure(0, weight=1)

  def start_new(self):
    if askyesno('Start New Game', 'Are you sure to start a new game?'):
      self.geometry('704x420')
      self.minsize(704, 420)

      self.container.destroy()

      self.draw_container()

      EntryPage(self.container, self.dict)

  def quit_game(self):
    if askyesno('Quit Game', 'Are you sure to quit the game?'):
      if self.child:
        self.child.destroy()

      self.quit()

  def set_geometry(self):
    if sys.platform == 'darwin':
      self.geometry('750x790')
      self.minsize(750, 790)
    elif sys.platform == 'win32':
      self.geometry('620x600')
      self.minsize(620, 600)
    else:
      self.geometry('700x650')
      self.minsize(700, 650)

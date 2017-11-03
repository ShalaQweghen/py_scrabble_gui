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

    about_m = Menu(top)
    about_m.add_command(label='Game Info', underline=0, command=self.render_info_page)
    about_m.add_command(label='License', underline=0, command=self.render_license_page)

    top.add_cascade(label='Game', menu=game_m, underline=0)
    top.add_cascade(label='About', menu=about_m, underline=0)

  def draw_container(self):
    self.container = Frame(self, bg='azure')
    self.container.pack(side=TOP, fill=BOTH, expand=YES)
    self.container.grid_rowconfigure(0, weight=1)
    self.container.grid_columnconfigure(0, weight=1)

  def render_info_page(self):
    info_page = Toplevel(self)
    info_page.minsize(700, 420)
    info_page.maxsize(700, 420)

    info = Text(info_page, height=40, width=90)
    scroll = Scrollbar(info_page, command=info.yview)

    info.configure(yscrollcommand=scroll.set)

    info.tag_configure('bold', font=('Arial', 15, 'bold'))
    info.tag_configure('title', font=('Arial', 21, 'bold', 'italic'), justify='center')
    info.tag_configure('italic', font=('Arial', 13, 'italic'))
    info.tag_configure('underline', font=('Arial', 12, 'italic', 'underline'))

    info.insert(END, 'BASIC INFO\n\n', 'title')
    info.insert(END, 'Blank Tile\n\n', 'bold')
    info.insert(END, 'Simply place a blank tile on the spot of the letter you want to replace it with. When you submit your word, a popup will ask you what letter it should be replaced with.\n\n\n')
    info.insert(END, 'Challenge Mode\n\n', 'bold')
    info.insert(END, 'The challenge mode is according to the double challenge rule. When activated, a player can challenge the words that the player before him or her has placed on the board. If one of the words is not valid, the previous player\'s turn will be passed and word points will be subtracted. If the words are valid, the turn of the player who has challenged will be passed.\n\n\n')
    info.insert(END, 'Multiplayer on a Single Machine\n\n', 'bold')
    info.insert(END, 'A game of 2, 3 or 4 players can be played on a single computer. The letters on the racks of the players will be concealed to prevent other players to see other players\' letters unintentionally. By clicking the ')
    info.insert(END, 'reveal', 'underline')
    info.insert(END, ' button, letters become visible. It is shown in red font above the board whose turn it is.\n\n\n')
    info.insert(END, 'Playing against Computer\n\n', 'bold')
    info.insert(END, 'Computer goes through permutations of letters on its rack and picks the valid move with the most points. A turn for computer takes about 1 minute 20 seconds (on i5 1.6 GHz with 8 GB RAM) depending on the computer.\n\nIf you want to end the game while it is computer\'s turn and try to close the program, you will have to wait till the computer\'s permutations are over, which takes about 1 minute (on i5 1.6 GHz with 8 GB RAM)\n\n\n')
    info.insert(END, 'Save a Game\n\n', 'bold')
    info.insert(END, 'If a game is saved during a LAN multiplayer game, it can be later loaded as a normal multiplayer game on a single machine.\n\n\n')
    info.insert(END, 'Multiplayer on LAN\n\n', 'bold')
    info.insert(END, 'Join a Game (Auto)', 'underline')
    info.insert(END, ' won\'t probably find the hosted game on networks which can assign more than 256 IP addresses (campus wifi and such). It might work if only the last part of the assigned IPs changes. In that case, ')
    info.insert(END, 'Join a Game (IP)', 'underline')
    info.insert(END, ' option can be used and the host IP address can be entered.\n\nIt is better to start a LAN game on a trusted network like a home or work network because security settings might prevent remote access on some systems.\n\nIf a player on an OS X machine wants to join a game on LAN, it is recommended to increase the size of open files. The limit is 256 on new versions and it will cause ')
    info.insert(END, '`OSError: [Errno 24] Too many open files`', 'italic')
    info.insert(END, ' because ')
    info.insert(END, 'Join a Game (Auto)', 'underline')
    info.insert(END, ' uses threads to scan all the available IP\'s on LAN. In order to increase the limit, use ')
    info.insert(END, '`ulimit -n <new_limit>`', 'italic')
    info.insert(END, '. Anything above 300 should suffice.\n\n\n')

    info.pack(side=LEFT, padx=20)
    scroll.pack(side=RIGHT, fill=Y)

  def render_license_page(self):
    l = open('LICENSE').read()

    license_page = Toplevel(self)
    license_page.minsize(680, 420)
    license_page.maxsize(680, 420)

    license = Text(license_page, height=40, width=80)
    scroll = Scrollbar(license_page, command=license.yview)

    license.configure(yscrollcommand=scroll.set)

    license.insert(END, l)

    license.pack(side=LEFT, padx=50)
    scroll.pack(side=RIGHT, fill=Y)

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
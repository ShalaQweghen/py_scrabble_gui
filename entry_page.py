from tkinter import *

from game_page import GamePage
from start_page import NormalStartPage, LANStartPage

class EntryPage(Frame):
  def __init__(self, parent):
    self.parent = parent
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

    Button(self, text='Load Game').pack(side=TOP, pady=30)


  def start_computer_game(self):
    self.parent.master.geometry("704x785")
    self.parent.master.minsize(704, 785)

    page = GamePage(self.parent, {'comp_mode': True, 'names': ['Player'], 'players': 1})
    page.tkraise()

  def start_normal_game(self):
    self.parent.master.geometry("704x420")
    self.parent.master.minsize(704, 420)

    page = NormalStartPage(self.parent)
    page.tkraise()


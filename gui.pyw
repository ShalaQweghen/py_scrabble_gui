#! /usr/local/bin/python3

from tkinter import *

from entry_page import EntryPage

class Root(Tk):
  def __init__(self):
    Tk.__init__(self)
    self.title('PyScrabble')
    self.config(bg='azure')
    self.iconbitmap('./pics/pyscrabble.ico')

    self.container = Frame(self, bg='azure')
    self.container.pack(side=TOP, fill=BOTH, expand=YES)
    self.container.grid_rowconfigure(0, weight=1)
    self.container.grid_columnconfigure(0, weight=1)

    self.draw_menu()

    EntryPage(self.container)

  def draw_menu(self):
    top = Menu(self)
    self.config(menu=top)

    game_m = Menu(top)
    game_m.add_command(label='New Game', underline=0, command=self.go_to_beginning)
    game_m.add_command(label='Load Game', underline=0)
    game_m.add_command(label='Quit', underline=0, command=self.quit)

    top.add_cascade(label='Game', menu=game_m, underline=0)

  def go_to_beginning(self):
    self.geometry("704x420")
    self.minsize(704, 420)

Root().mainloop()

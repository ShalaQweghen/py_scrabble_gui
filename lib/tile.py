from tkinter import *

class Tile(Frame):
  def __init__(self, row, col, parent=None, letter='', **options):
    self.var = StringVar()
    self.var.set(letter)

    Frame.__init__(self, parent, **options)
    self.grid(row=row, column=col)

    self.label = Label(self, textvariable=self.var)
    self.label.config(bd=1, height=2, width=4, relief=SUNKEN)
    self.label.pack()
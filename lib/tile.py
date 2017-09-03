from tkinter import *

class Tile(Frame):
  def __init__(self, row, col, parent=None, text='', **options):
    Frame.__init__(self, parent, **options)
    self.grid(row=row, column=col)
    self.label = Label(self, text=text)
    self.label.config(bd=1, height=2, width=4, relief=SUNKEN)
    self.label.pack()
    self.label.bind('<Button-1>', lambda event: print(event.widget, event.x, event.y))
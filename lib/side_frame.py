from tkinter import *

class SideFrame(Frame):
  def __init__(self, fside, arange, parent=None, **options):
    Frame.__init__(self, parent, **options)
    self.pack(side=fside)
    if fside == TOP or fside == BOTTOM:
      lside = LEFT

      Label(self, bd=1, height=2, width=4, relief=RIDGE).pack(side=LEFT)
      Label(self, bd=1, height=2, width=4, relief=RIDGE).pack(side=RIGHT)
    else:
      lside = TOP

    com = str if 1 in arange else chr

    for i in arange:
      label = Label(self, text=com(i))
      label.config(bd=1, height=2, width=4, relief=RIDGE)
      label.pack(side=lside)

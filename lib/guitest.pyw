from tkinter import *
from tkinter.messagebox import *
from tile import Tile

def notdone():
  showerror('Not implemented', 'Not yet available')

root = Tk()

top = Menu(root)
root.config(menu=top)

file = Menu(top)

submenu = Menu(file, tearoff=True)
submenu.add_command(label='With Comp', command=notdone, underline=0)
submenu.add_command(label='On This Computer', command=notdone, underline=0)
submenu.add_command(label='On LAN', command=notdone, underline=0)
file.add_cascade(label='New Game', menu=submenu, underline=0)

file.add_command(label='Load Game', command=notdone, underline=0)
file.add_command(label='Quit', command=root.quit, underline=0)
top.add_cascade(label='Game', menu=file, underline=0)

th = Frame(root)
th.pack(side=TOP)
Label(th, text='', bd=1, height=2, width=4, relief=RIDGE).pack(side=LEFT)
for i in range(97, 112):
  Label(th, text=chr(i), bd=1, height=2, width=4, relief=RIDGE).pack(side=LEFT)
Label(th, text='', bd=1, height=2, width=4, relief=RIDGE).pack(side=LEFT)

bh = Frame(root)
bh.pack(side=BOTTOM)
Label(bh, text='', bd=1, height=2, width=4, relief=RIDGE).pack(side=LEFT)
for i in range(97, 112):
  Label(bh, text=chr(i), bd=1, height=2, width=4, relief=RIDGE).pack(side=LEFT)
Label(bh, text='', bd=1, height=2, width=4, relief=RIDGE).pack(side=LEFT)

lh = Frame(root)
lh.pack(side=LEFT)
for i in range(1, 16):
  Label(lh, text=str(i), bd=1, height=2, width=4, relief=RIDGE).pack(side=BOTTOM)

rh = Frame(root)
rh.pack(side=RIGHT)
for i in range(1, 16):
  Label(rh, text=str(i), bd=1, height=2, width=4, relief=RIDGE).pack(side=BOTTOM)

boardframe = Frame(root)
boardframe.pack()

start = None

def handleEvent(event):
  global start

  if start:
    event.widget.master.var.set(start.get())
    start = None
  else:
    start = event.widget.master.var

c = range(97, 112)
r = range(1, 16)
row = 0
while row < 15:
  col = 0
  while col < 15:
    t = Tile(row, col, boardframe)
    t.label.bind('<1>', handleEvent)
    col += 1
  row += 1


root.title('PyScrabble')
root.config(height=1000, width=1000)
root.mainloop()


from tkinter import *
from tkinter.messagebox import *

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

boarframe = Frame(root, pady=10)
boarframe.pack()


root.title('PyScrabble')
root.config(height=1000, width=1000)
root.mainloop()


from typers.typingsimulator import tkinter
from typers.timedtyping import TimedTyping
from random import shuffle

window = tkinter.Tk()

with open('lines.txt', 'r') as file:
    all_lines = file.readlines()

shuffle(all_lines)
lines_gen = (line for line in all_lines)

typing_sim = TimedTyping(window, lines_gen)

window.mainloop()

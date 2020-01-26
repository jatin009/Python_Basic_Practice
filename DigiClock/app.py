import tkinter as tk
from datetime import datetime

window = tk.Tk()
window.geometry("50x50")

hour_text_var = tk.StringVar(window)

def updateTime():
    hour_text_var.set(datetime.now().strftime("%H:%M:%S"))
    lbl.after(1000, updateTime)    

lbl = tk.Label(window,
              textvariable=hour_text_var,
              fg="black",
              bg="white",
              font=("Arial", 20))
lbl.pack(side="left", fill="x")

updateTime()

window.mainloop()

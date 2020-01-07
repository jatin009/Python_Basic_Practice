import tkinter

window = tkinter.Tk()
window.title("Calculator App")
window.geometry("360x355")
window.resizable(False, False)

text_var = tkinter.StringVar(window)
first_value = 0
operation_selected = None
operation_done = False
receving_second_num = False

def put_decimal():
    if '.' not in text_var.get():
        text_var.set(text_var.get() + '.')


def button_press(button_id):
    global operation_done
    global receving_second_num

    # just a case to prevent below elif from occuring
    if receving_second_num:
        pass

    # reset the field in case of one of +,-,*,/ operations selected so that second number could be entered
    elif operation_selected:
        text_var.set('')
        receving_second_num = True

    # or one of these operations has just finished
    elif operation_done:
        text_var.set('')
        operation_done = False
        receving_second_num = False

    text_var.set(text_var.get() + str(button_id))


def operation(type):
    global first_value
    global operation_selected
    global operation_done
    global receving_second_num

    operation_done = False

    if text_var.get() == '':
        return

    if type == 'clear':
        text_var.set('')
        first_value = 0
        operation_selected = None
        operation_done = False
        return

    # operation result expected
    if type == 'equal' and first_value:
        curr_value = float(text_var.get())

        if operation_selected == 'add':
            text_var.set(curr_value + first_value)
        elif operation_selected == 'sub':
            text_var.set(first_value - curr_value)
        elif operation_selected == 'mul':
            text_var.set(curr_value * first_value)
        elif operation_selected == 'div':
            if curr_value > 0.0:
                text_var.set(first_value / curr_value)

        operation_selected = None
        operation_done = True
        receving_second_num = False

    # add, mul, div, sub operation selected
    elif type != 'equal':
        first_value = float(text_var.get())
        operation_selected = type


# text area
lbl = tkinter.Label(window, textvariable=text_var, fg="black", bg="lightgrey", font=("Arial", 20), anchor='se', padx=5,
                    pady=3, height=2).grid(columnspan=4, sticky="we")

# ---- Grid of buttons -----

# first row
btn1 = tkinter.Button(window, text="1", fg="black", bg="white", font=("Arial", 20), height=1, width=5,
                      command=lambda: button_press(1)).grid(column=0, row=4)
btn1 = tkinter.Button(window, text="2", fg="black", bg="white", font=("Arial", 20), height=1, width=5,
                      command=lambda: button_press(2)).grid(column=1, row=4)
btn1 = tkinter.Button(window, text="3", fg="black", bg="white", font=("Arial", 20), height=1, width=5,
                      command=lambda: button_press(3)).grid(column=2, row=4)
btn1 = tkinter.Button(window, text="+", fg="black", bg="white", font=("Arial", 20), height=1, width=5,
                      command=lambda: operation('add')).grid(column=3, row=4)

# second row
btn1 = tkinter.Button(window, text="7", fg="black", bg="white", font=("Arial", 20), height=1, width=5,
                      command=lambda: button_press(7)).grid(column=0, row=2)
btn1 = tkinter.Button(window, text="8", fg="black", bg="white", font=("Arial", 20), height=1, width=5,
                      command=lambda: button_press(8)).grid(column=1, row=2)
btn1 = tkinter.Button(window, text="9", fg="black", bg="white", font=("Arial", 20), height=1, width=5,
                      command=lambda: button_press(9)).grid(column=2, row=2)
btn1 = tkinter.Button(window, text="-", fg="black", bg="white", font=("Arial", 20), height=1, width=5,
                      command=lambda: operation('sub')).grid(column=3, row=2)

# third row
btn1 = tkinter.Button(window, text="4", fg="black", bg="white", font=("Arial", 20), height=1, width=5,
                      command=lambda: button_press(4)).grid(column=0, row=3)
btn1 = tkinter.Button(window, text="5", fg="black", bg="white", font=("Arial", 20), height=1, width=5,
                      command=lambda: button_press(5)).grid(column=1, row=3)
btn1 = tkinter.Button(window, text="6", fg="black", bg="white", font=("Arial", 20), height=1, width=5,
                      command=lambda: button_press(6)).grid(column=2, row=3)
btn1 = tkinter.Button(window, text="*", fg="black", bg="white", font=("Arial", 20), height=1, width=5,
                      command=lambda: operation('mul')).grid(column=3, row=3)

# fourth row
btn1 = tkinter.Button(window, text="C", fg="black", bg="white", font=("Arial", 20),
                      command=lambda: operation('clear')).grid(column=0, row=1, columnspan=3, sticky="we")
btn1 = tkinter.Button(window, text="/", fg="black", bg="white", font=("Arial", 20), height=1, width=5,
                      command=lambda: operation('div')).grid(column=3, row=1)

# fifth row
btn1 = tkinter.Button(window, text="0", fg="black", bg="white", font=("Arial", 20),
                      command=lambda: button_press(0)).grid(column=0, row=5, columnspan=2, sticky="we")
btn1 = tkinter.Button(window, text=".", fg="black", bg="white", font=("Arial", 20), height=1, width=5,
                      command=put_decimal).grid(column=2, row=5)
btn1 = tkinter.Button(window, text="=", fg="black", bg="white", font=("Arial", 20), height=1, width=5,
                      command=lambda: operation('equal')).grid(column=3, row=5)

window.mainloop()

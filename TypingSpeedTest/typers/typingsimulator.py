import tkinter
import tkinter.font as font
import time


class TypingSimulator:

    SECS_IN_MIN = 60

    def __init__(self, master):
        self.master = master
        self.master.title("Typing Speed Test")
        self.master.geometry("600x600")
        self.master.resizable(False, False)
        # set window background color
        self.master.configure(bg="black")

        # metrics variables
        self.typing_started = False
        self.start_time = 0
        self.end_time = 0
        self.words_typed = 0

        # to detect any key press on window
        self.master.bind('<KeyPress>', self.on_key_press)

        # input output string variables
        self.input_var = tkinter.StringVar(self.master)
        self.output_var = tkinter.StringVar(self.master)

        # 1! heading label
        tkinter.Label(self.master, text="Typing Speed Test", fg="#F7AF56", bg="black",
                      font=("Arial", 30)).pack(padx=5, pady=55)

        # 2! typing string label
        tkinter.Label(self.master,text='India is a great country. I love my India. Shobhit is my brother forever.',
                      fg="white", bg="black", font=("Arial", 12)).pack(padx=5, pady=25)

        # 3! user typing frame
        frame = tkinter.Frame(self.master, bg="black", highlightbackground="#F7AF56", highlightcolor="#F7AF56",
                              highlightthickness=2,
                              width=525, height=60)
        frame.pack(fill=None, expand=False, pady=40)
        frame.pack_propagate(False)
        input_lbl = tkinter.Label(frame, textvariable=self.input_var, fg="white", bg="black", font=("Arial", 12))
        input_lbl.pack(pady=5)

        # 4! typing metrics output
        output_lbl = tkinter.Label(self.master, textvariable=self.output_var, fg="red", bg="black",
                                   font=("Arial", 12))
        output_lbl.pack(padx=10, pady=40)

        # 5! reset button frame
        self.reset_frame = tkinter.Frame(self.master, bg="black")
        self.reset_frame.pack()
        self.reset_btn = tkinter.Button(self.master, text="Reset", fg="black", bg="#F7AF56",
                                        command=self.reset_clicked)
        self.reset_btn['font'] = font.Font(family='Helvetica', size=12, weight="bold")
        self.reset_btn.pack(padx=10, pady=30, in_=self.reset_frame)
        # hide reset button
        self.reset_btn.lower(self.reset_frame)

    def on_key_press(self, event):

        # Do not accept anything once enter is pressed and end-time recorded
        if self.end_time != 0:
            return
        prev_content = self.input_var.get()

        # Enter pressed to submit the text entered
        if event.keysym == 'Return':
            self.calc_typing_data()
        # Enabling backspace to do its usual job
        elif event.keysym == 'BackSpace':
            self.input_var.set(prev_content[:-1])
            self.words_typed -= 1
        else:
            self.input_var.set(prev_content + event.char)
            if event.keysym != 'space':
                self.words_typed += 1
            # check to store time the first letter is typed
            if not self.typing_started:
                self.typing_started = True
                self.start_time = time.time()

    def calc_typing_data(self):
        self.end_time = time.time()

        words_per_min = (self.words_typed/5) / ((self.end_time - self.start_time)/self.SECS_IN_MIN)
        output_str = f"Time: {self.end_time - self.start_time:.2f} secs\tAccuracy: 22%\tWpm: {words_per_min:.2f}"
        self.output_var.set(output_str)

        # show reset button
        self.reset_btn.lift(self.reset_frame)

    def reset_clicked(self):
        self.start_time = 0
        self.end_time = 0
        self.words_typed = 0
        self.typing_started = False
        self.input_var.set('')
        self.output_var.set('')

        # hide reset button
        self.reset_btn.lower(self.reset_frame)

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
from text import get_font


class WaitingAfterQuestionScreen(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.message_label = tk.Label(self, font=get_font(12), fg='white')
        self.message_label.pack(side='bottom', pady=16)

        self.info_label = tk.Label(self, font=get_font(36), fg='white')
        self.info_label.pack(anchor='center', fill="both", pady=128)

    def set_correct(self, correct, message):
        self.message_label.config(text=message)
        self.info_label.config(text='Correct' if correct else 'Wrong')
        if correct:
            color = 'green'
        else:
            color = 'red'

        self.config(bg=color)
        self.message_label.config(bg=color)
        self.info_label.config(bg=color)

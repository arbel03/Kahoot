try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

from Client.view.text import *
from Common.model import Question


class ButtonsPane(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.button1 = None
        self.button2 = None
        self.button3 = None
        self.button4 = None

        self.init_buttons()

    def init_buttons(self):
        self.button1 = tk.Button(self, background='#e21b3c', font=get_font(), fg='white')
        self.button2 = tk.Button(self, background='#1368ce', font=get_font(), fg='white')
        self.button3 = tk.Button(self, background='#ffa602', font=get_font(), fg='white')
        self.button4 = tk.Button(self, background='#298f0d', font=get_font(), fg='white')

        self.button1.grid(row=0, column=0, sticky='NSEW', padx=8, pady=8)
        self.button2.grid(row=0, column=1, sticky='NSEW', padx=8, pady=8)
        self.button3.grid(row=1, column=0, sticky='NSEW', padx=8, pady=8)
        self.button4.grid(row=1, column=1, sticky='NSEW', padx=8, pady=8)

        self.button1.grid_propagate(0)
        self.button2.grid_propagate(0)
        self.button3.grid_propagate(0)
        self.button4.grid_propagate(0)

    def set_button_callback(self, callback):
        self.button1.config(command=lambda: callback(0))
        self.button2.config(command=lambda: callback(1))
        self.button3.config(command=lambda: callback(2))
        self.button4.config(command=lambda: callback(3))

    def enable(self):
        self.button1.config(state=tk.NORMAL)
        self.button2.config(state=tk.NORMAL)
        self.button3.config(state=tk.NORMAL)
        self.button4.config(state=tk.NORMAL)

    def disable(self):
        self.button1.config(state=tk.DISABLED)
        self.button2.config(state=tk.DISABLED)
        self.button3.config(state=tk.DISABLED)
        self.button4.config(state=tk.DISABLED)

    def set_buttons_labels_strings(self, answers):
        self.button1.config(text=html_decode(answers[0].answer))
        self.button2.config(text=html_decode(answers[1].answer))
        self.button3.config(text=html_decode(answers[2].answer))
        self.button4.config(text=html_decode(answers[3].answer))


class InfoPane(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.time_label = tk.Label(self, text="00:20", font=get_font())
        self.question_label = tk.Label(self, text="Question will appear here...", font=get_font(36))

        self.set_widgets()

    def set_widgets(self):
        self.time_label.pack(side='top', anchor='nw')
        self.question_label.pack(fill='both', anchor='center', expand=True)
        self.question_label.pack_propagate(0)

    def set_question(self, text):
        self.question_label.config(text=html_decode(text))

    def update_time_label(self, seconds_left):
        self.time_label.config(text='%02d:%02d' % (seconds_left/60, seconds_left % 60))


class GameScreen(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.buttons = ButtonsPane(self)
        self.info_pane = InfoPane(self)

        self.set_geometry()
        self.set_widgets()

    def set_geometry(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2)
        self.columnconfigure(0, weight=1)

    def set_widgets(self):
        self.buttons.grid_propagate(0)
        self.buttons.grid(row=1, column=0, pady=16, padx=16, sticky='NSEW')
        self.info_pane.grid(row=0, column=0, pady=16, padx=32, sticky='NSEW')

    def update_question(self, question):
        if isinstance(question, Question):
            answers = question.get_answers()
            # Setting shuffled button labels
            self.buttons.set_buttons_labels_strings(answers)
            # Setting question label
            self.info_pane.set_question(question.question)
            return answers

    def update_countdown(self, time):
        self.info_pane.update_time_label(time)

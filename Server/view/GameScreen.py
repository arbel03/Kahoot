import Tkinter as tk
from font import get_font


class ButtonsPane(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.set_buttons()

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def set_buttons(self):
        triangle = tk.Button(self, background='#e21b3c', font=get_font(), fg='white')
        diamond = tk.Button(self, background='#1368ce', font=get_font(), fg='white')
        circle = tk.Button(self, background='#ffa602', font=get_font(), fg='white')
        square = tk.Button(self, background='#298f0d', font=get_font(), fg='white')

        triangle.grid(row=0, column=0, sticky='NSEW', padx=8, pady=8)
        diamond.grid(row=0, column=1, sticky='NSEW', padx=8, pady=8)
        circle.grid(row=1, column=0, sticky='NSEW', padx=8, pady=8)
        square.grid(row=1, column=1, sticky='NSEW', padx=8, pady=8)


class InfoPane(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.time_label = tk.Label(self, text="00:20", font=get_font())
        self.question_label = tk.Label(self, text="Question will appear here...", font=get_font(36))

        self.set_widgets()

    def set_widgets(self):
        self.time_label.pack(side='top', anchor='nw')
        self.question_label.pack(fill='both', anchor='center', expand=True)


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
        self.buttons.grid(row=1, column=0, pady=16, padx=16, sticky='NSEW')
        self.info_pane.grid(row=0, column=0, pady=16, padx=32, sticky='NSEW')

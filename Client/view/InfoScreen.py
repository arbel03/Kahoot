import Tkinter as tk
from Common.text import get_font


class InfoScreen(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.info_label = tk.Label(self, font=get_font(36))
        self.setup()

    def setup(self):
        self.info_label.pack(fill='x', pady=32, anchor='center', side='top')

    def set_text(self, text):
        self.info_label.config(text=text)
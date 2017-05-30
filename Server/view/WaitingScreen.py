import Tkinter as tk
from Common.text import get_font


class UsernamesWall(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.columns = 5
        self.labels = []
        self.set_geometry()

    def set_geometry(self):
        for i in range(0, 5):
            self.grid_columnconfigure(i, weight=1)
        for i in range(0, 5):
            self.grid_rowconfigure(i, weight=1)

    def add_label(self):
        return tk.Label(self, background='#ADD8E6', foreground='white', font=get_font(28))

    def update_usernames(self, names):
        # Adding labels the amount we need
        while len(names) > len(self.labels):
            self.labels.append(self.add_label())

        # Removing all labels
        for i in self.labels:
            i.grid_forget()

        # Adding labels the amount we actually need
        for i in range(0, len(names)):
            self.labels[i].config(text=names[i])
            self.labels[i].grid(row=i / self.columns, column=i % self.columns, sticky="NEWS", padx=16, pady=8)


class WaitingScreen(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.usernames_wall = UsernamesWall(self)
        self.info_label = tk.Label(self, text="Waiting for players...", font=get_font(36))
        self.set_geometry()
        self.set_widgets()

    def set_geometry(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=5)
        self.grid_columnconfigure(0, weight=1)

    def set_widgets(self):
        self.info_label.grid(row=0, column=0, sticky="NSEW")
        self.usernames_wall.grid(row=1, column=0, sticky="NSEW")

    def update_usernames(self, names):
        self.usernames_wall.update_usernames(names)

    def set_info_label(self, text):
        self.info_label.config(text=text)

    def update_countdown(self, time_to_start):
        self.set_info_label('Game starting in ' + str(time_to_start) + ' seconds.')

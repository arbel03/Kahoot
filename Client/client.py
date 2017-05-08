import Tkinter as tk
import thread
import time

class ButtonsPane(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.set_buttons()

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def get_font(self, size=20):
        import tkFont
        return tkFont.Font(family='Helvetica Light', size=size)

    def set_buttons(self):
        triangle = tk.Button(self, background='#e21b3c', font=self.get_font(), fg='white')
        diamond = tk.Button(self, background='#1368ce', font=self.get_font(), fg='white')
        circle = tk.Button(self, background='#ffa602', font=self.get_font(), fg='white')
        square = tk.Button(self, background='#298f0d', font=self.get_font(), fg='white')

        triangle.grid(row=0, column=0, sticky='NSEW', padx=8, pady=8)
        diamond.grid(row=0, column=1, sticky='NSEW', padx=8, pady=8)
        circle.grid(row=1, column=0, sticky='NSEW', padx=8, pady=8)
        square.grid(row=1, column=1, sticky='NSEW', padx=8, pady=8)

class InfoPane(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.time_label = tk.Label(self, text="00:20", font=self.get_font(), bg=None)
        self.question_label = tk.Label(self, text="Question will appear here...", font=self.get_font(36), bg=None)

        self.layout()

    def get_font(self, size=20):
        import tkFont
        return tkFont.Font(family='Helvetica Bold', size=size)

    def layout(self):
        self.time_label.pack(side='top', anchor='nw')
        self.question_label.pack(fill='both', anchor='center', expand=True)

class KahootClientView(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.title('Kahoot')
        self.buttons = ButtonsPane(self, bg='')
        self.info_pane = InfoPane(self, bg='')

        self.set_geometry(1000, 600)
        self.set_widgets()
        self.change_background_color()

    def set_geometry(self, width, height):
        self.parent.update_idletasks()
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        x = screen_width / 2 - width / 2
        y = screen_height / 2 - height / 2
        self.parent.geometry("%dx%d+%d+%d" % (width, height, x, y))

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2)
        self.columnconfigure(0, weight=1)

    def set_widgets(self):
        self.buttons.grid(row=1, column=0, pady=16, padx=16, sticky='NSEW')
        self.info_pane.grid(row=0, column=0, pady=16, padx=32, sticky='NSEW')

    def change_background_color(self):
        colors = [
        '#45a3e5',
        '#66bf39',
        '#eb670f',
        '#f35',
        '#864cbf'
        ]
        self.configure(background=colors[0])
        thread.start_new_thread(self.change_color, (colors,))

    def change_color(self, colors):
        i = 1
        while 1:
            self.configure(background=colors[i % len(colors)])
            self.info_pane.configure(background=colors[i % len(colors)])
            self.buttons.configure(background=colors[i % len(colors)])
            self.info_pane.time_label.configure(background=colors[i % len(colors)])
            self.info_pane.question_label.configure(background=colors[i % len(colors)])

            time.sleep(5)
            i += 1
        threa.exit

def main():
    root = tk.Tk()
    KahootClientView(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

if __name__ == "__main__":
    main()

from ThreadedSocketServer.Server import ThreadedSocketServer
import Tkinter as tk

class KahootServer(ThreadedSocketServer):
    
    def __init__(self, port):
        ThreadedSocketServer.__init__(self, port)
    
    def onmessage(self, client, message):
        print "Client Sent Message"
        #Sending message to all clients
        self.broadcast(message)
    
    def onopen(self, client):
        print "Client Connected"
    
    def onclose(self, client):
        print "Client Disconnected"

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
        self.time_label = tk.Label(self, text="00:20", font=self.get_font())
        self.question_label = tk.Label(self, text="Question will appear here...", font=self.get_font(36))

        self.layout()

    def get_font(self, size=20):
        import tkFont
        return tkFont.Font(family='Helvetica Bold', size=size)

    def layout(self):
        self.time_label.pack(side='top', anchor='nw')
        self.question_label.pack(fill='both', anchor='center', expand=True)

class KahootServerView(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.buttons = ButtonsPane(self)
        self.info_pane = InfoPane(self)

        self.set_geometry()
        self.set_widgets()

    def set_geometry(self):
        self.parent.attributes('-fullscreen', True)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2)
        self.columnconfigure(0, weight=1)

    def set_widgets(self):
        self.buttons.grid(row=1, column=0, pady=16, padx=16, sticky='NSEW')
        self.info_pane.grid(row=0, column=0, pady=16, padx=32, sticky='NSEW')

def main():
    #port = 8080
    #server = KahootServer(port)
    #server.run()
    root = tk.Tk()
    KahootServerView(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

if __name__ == "__main__":
    main()

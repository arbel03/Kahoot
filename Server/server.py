from ThreadedSocketServer.Server import ThreadedSocketServer
import Tkinter as tk
import thread
import time

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

class AnswerButton(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

class KahootServerView(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.set_geometry()
        self.set_background()
        self.set_widgets()

    def set_geometry(self):
        self.parent.attributes('-fullscreen', True)

    def set_background(self):
        self.configure(background='#FF00FF')

    def set_widgets(self):
        pass

def main():
    #port = 8080
    #server = KahootServer(port)
    #server.run()
    root = tk.Tk()
    KahootServerView(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

if __name__ == "__main__":
    main()

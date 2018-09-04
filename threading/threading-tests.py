import random
import thread
import threading
import tkinter

"""
thread.start_new_thread(entry_function, args = (), kwargs = {})
    -> starts a new thread
thread.exit()
    -> exits the current thread
"""

class Callback:
    """
    a callable callback
    so we can remember which widget the callback is for
    """
    
    def __init__(self, widget):
        self.widget = widget

    def __call__(self, event):
        print "event detected at", (event.x, event.y)

class RandomBG(Callback):
    """set a random background color for the widget"""
    COLORS = ("red", "orange", "yellow", "green", "blue", "indigo", "violet")
    
    def __init__(self, *args, **kwargs):
        Callback.__init__(self, *args, **kwargs)
    
    def __call__(self, event):
        """execute the callback"""
        Callback.__call__(self, event)
        
        new_bg = random.choice(self.COLORS)

        while new_bg == self.widget.cget("background"):
            new_bg = random.choice(self.COLORS)
        self.widget.configure(background = new_bg)
        print "setting background to", new_bg

class RandomBGWithWork(RandomBG):
    """do some work after setting the background color"""

    def __init__(self, *args, **kwargs):
        RandomBG.__init__(self, *args, **kwargs)

    def __call__(self, event):
        RandomBG.__call__(self, event)
        n = random.randint(1, 10 ** 8)
        print "doing %u iterations of work" % n

        while n > 0:
            n -= 1

window = tkinter.Tk()
frame = tkinter.Frame(window, height = 100, width = 100)
frame.bind("<Button-1>", RandomBGWithWork(frame).__call__)
frame.pack()
window.mainloop()

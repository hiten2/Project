import thread
import threading
import tkinter

"""
thread.start_new_thread(entry_function, args = (), kwargs = {})
    -> starts a new thread
thread.exit()
    -> exits the current thread
"""

def callback(event):
    print "event detected at", (event.x, event.y)

window = tkinter.Tk()
frame = tkinter.Frame(window, height = 100, width = 100)
frame.bind("<Button-1>", callback)
frame.pack()

window.mainloop()

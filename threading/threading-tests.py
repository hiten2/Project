import thread
import threading
import tkinter

"""
thread.start_new_thread(entry_function, args = (), kwargs = {})
    -> starts a new thread
thread.exit()
    -> exits the current thread
"""

def space_callback(event):
    print 1

window = tkinter.Tk()
frame = tkinter.Frame(window, height = 100, width = 100)
frame.bind("<Button1-Down>", space_callback)
window.mainloop()

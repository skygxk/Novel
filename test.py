import tkinter

def display(e):
    print(e.keysym)

win = tkinter.Tk()
win.bind_all("<KeyPress>", display)
win.mainloop()
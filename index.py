# -*- coding:utf-8 -*-
import tkinter
from tkinter import font
import novelreader as nr

def test(event):
    print(event.keycode)
    exit()

class System:
    def __init__(self):
        self.set_up()
        self.set_novel(nr.get_settings('name'))
        self.win.mainloop()

    def set_up(self):
        self.win = tkinter.Tk()
        self.width = self.win.winfo_screenwidth()
        self.height = self.win.winfo_screenheight()
        self.win.title('novel system')
        self.win.geometry("%dx%d" % (self.width, self.height))
        self.win.focus_set()
        # self.win.overrideredirect(1)
        self.win.bind_all("<Up>", self.page_up)
        self.win.bind_all("<Down>", self.page_down)
        self.win.bind_all("<Left>", self.page_left)
        self.win.bind_all("<Right>", self.page_right)

        self.win.bind_all("<w>", self.page_up)
        self.win.bind_all("<s>", self.page_down)
        self.win.bind_all("<a>", self.page_left)
        self.win.bind_all("<d>", self.page_right)

        self.win.bind_all("<space>", self.page_down)
        self.win.bind_all("<Return>", self.page_right)
        self.win.bind_all("<Escape>", self.close)

        self.page = tkinter.Text(self.win)
        self.page.place(relx=0.2,rely=0.01,relwidth=0.6,relheight=0.98)
        self.page['bd'] = -1
        self.page['cursor'] = 'arrow'
        self.set_text()
        self.set_font_size(nr.get_settings('font_size'))
        self.set_backcolor(nr.get_settings('backcolor'))
        self.set_forecolor(nr.get_settings('forecolor'))

    def close(self, event):
        exit(0)

    def page_up(self, event):
        self.page.yview_scroll(-1, "pages")

    def page_down(self, event):
        self.page.yview_scroll(1, "pages")

    def page_left(self, event):
        self.set_text(nr.get_last_chapter(self.contents, self.lines))

    def page_right(self, event):
        self.set_text(nr.get_next_chapter(self.contents, self.lines))

    def set_text(self, text=''):
        self.page['state'] = tkinter.NORMAL
        self.page.delete(0.0, tkinter.END)
        self.page.insert(0.0, text)
        self.page['state'] = tkinter.DISABLED

    def set_backcolor(self, color='#b8e392'):
        self.page['bg'] = color
        self.win['bg'] = color
        nr.set_settings('backcolor', color)

    def set_forecolor(self, color='#000000'):
        self.page['fg'] = color
        nr.set_settings('forecolor', color)

    def set_font_size(self, size=30):
        self.page['font'] = font.Font(size=size)
        self.page['spacing2'] = size/2
        self.page['spacing3'] = size*1.5
        nr.set_settings('font_size', size)

    def set_novel(self, name):
        nr.set_settings('name', name)
        self.contents = nr.get_contents()
        self.lines = nr.get_lines()
        self.set_text(nr.get_this_chapter(self.contents, self.lines))

system = System()

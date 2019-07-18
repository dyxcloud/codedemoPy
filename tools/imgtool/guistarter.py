import os
import sys
from tkinter import *
from tkinter import scrolledtext
from tkinter.font import Font
from tkinter.messagebox import *
from tkinter.ttk import *

from tools.imgtool import mytool

#import tkinter.filedialog as tkFileDialog
#import tkinter.simpledialog as tkSimpleDialog    #askstring()

class Application_ui(Frame):
    #这个类仅实现界面生成功能，具体事件处理代码在子类Application中。
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('图片转Base64')
        self.master.geometry('406x150')
        self.createWidgets()

    def createWidgets(self):
        self.top = self.winfo_toplevel()

        self.style = Style()

        self.data_url = StringVar(value='')
        self.Text1 = Entry(self.top, textvariable=self.data_url, font=('微软雅黑',9))
        self.Text1.place(relx=0.040, rely=0.070, relwidth=0.500, relheight=0.180)

        self.style.configure('Command1.TButton',font=('微软雅黑',9))
        self.Command1 = Button(self.top, text='上传', command=self.doupload, style='Command1.TButton')
        self.Command1.place(relx=0.571, rely=0.070, relwidth=0.120, relheight=0.180)

        self.style.configure('Command2.TButton',font=('微软雅黑',9))
        self.Command2 = Button(self.top, text='转换', command=self.dotrans, style='Command2.TButton')
        self.Command2.place(relx=0.730, rely=0.070, relwidth=0.230, relheight=0.180)

        self.data_checkps = StringVar(value='0')
        self.style.configure('Check1.TCheckbutton',font=('微软雅黑',9))
        self.Check1 = Checkbutton(self.top, text='进行图片压缩', variable=self.data_checkps, style='Check1.TCheckbutton')
        self.Check1.place(relx=0.040, rely=0.300, relwidth=0.400, relheight=0.150)

        # self.style.configure('Label1.TLabel',anchor='w', font=('微软雅黑',9))
        # self.Label1 = Label(self.top, text='进行图片压缩', style='Label1.TLabel')
        # self.Label1.place(relx=0.120, rely=0.300, relwidth=0.500, relheight=0.150)

        self.copytext = StringVar(value='点击复制')
        self.style.configure('Command2.TButton',font=('微软雅黑',9))
        self.Command3 = Button(self.top, textvariable =self.copytext, command=self.docopy, style='Command3.TButton')
        self.Command3.place(relx=0.040, rely=0.500, relwidth=0.920, relheight=0.430)


class Application(Application_ui):
    #这个类实现具体的事件处理回调函数。界面生成代码在Application_ui中。
    def __init__(self, master=None):
        Application_ui.__init__(self, master)

    result = ""

    def doupload(self, event=None):
        self.copytext.set("making...")
        check = int(self.data_checkps.get())
        if check:
            self.result,showlen = mytool.work_file_compression("")
        else:
            self.result,showlen = mytool.work_file("")
        if len(self.result)>50:
            addToClipBoard(self.result)
            self.copytext.set("点击复制, "+showlen)
        else:
            self.copytext.set("fail!")

    def dotrans(self, event=None):
        self.copytext.set("making...")
        dataurl = self.data_url.get()
        check = int(self.data_checkps.get())
        if check:
            self.result,showlen = mytool.work_url_compression(dataurl)
        else:
            self.result,showlen = mytool.work_url(dataurl)
        if len(self.result)>50:
            addToClipBoard(self.result)
            self.copytext.set("点击复制, "+showlen)
        else:
            self.copytext.set("fail!")
    
    def docopy(self, even=None):
        addToClipBoard(self.result)


def addToClipBoard(text):
        # command = 'echo ' + text + '| clip'
        # os.system(command)
        r = Tk()
        r.withdraw()
        r.clipboard_clear()
        r.clipboard_append(text)
        r.update()
        r.destroy()

if __name__ == "__main__":
    #text很卡
    #换成复制按钮
    top = Tk()
    Application(top).mainloop()
    top.destroy()

import os
import sys
from tkinter import *
from tkinter import scrolledtext
from tkinter.font import Font
from tkinter.messagebox import *
from tkinter.ttk import *

import mytool

#import tkinter.filedialog as tkFileDialog
#import tkinter.simpledialog as tkSimpleDialog    #askstring()

class Application_ui(Frame):
    #这个类仅实现界面生成功能，具体事件处理代码在子类Application中。
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('图片转Base64')
        self.master.geometry('406x218')
        self.createWidgets()

    def createWidgets(self):
        self.top = self.winfo_toplevel()

        self.style = Style()

        self.data_url = StringVar(value='')
        self.Text1 = Entry(self.top, textvariable=self.data_url, font=('微软雅黑',9))
        self.Text1.place(relx=0.039, rely=0.073, relwidth=0.495, relheight=0.188)

        self.style.configure('Command1.TButton',font=('微软雅黑',9))
        self.Command1 = Button(self.top, text='上传', command=self.doupload, style='Command1.TButton')
        self.Command1.place(relx=0.571, rely=0.073, relwidth=0.121, relheight=0.188)

        self.style.configure('Command2.TButton',font=('微软雅黑',9))
        self.Command2 = Button(self.top, text='转换', command=self.dotrans, style='Command2.TButton')
        self.Command2.place(relx=0.729, rely=0.073, relwidth=0.239, relheight=0.188)

        self.data_checkps = StringVar(value='0')
        self.style.configure('Check1.TCheckbutton',font=('微软雅黑',9))
        self.Check1 = Checkbutton(self.top, text='Check1', variable=self.data_checkps, style='Check1.TCheckbutton')
        self.Check1.place(relx=0.079, rely=0.257, relwidth=0.042, relheight=0.115)

        self.style.configure('Label1.TLabel',anchor='w', font=('微软雅黑',9))
        self.Label1 = Label(self.top, text='使用PSCC进行图片压缩', style='Label1.TLabel')
        self.Label1.place(relx=0.118, rely=0.294, relwidth=0.475, relheight=0.115)

        #self.data_result = StringVar(value='')
        self.Text2 = scrolledtext.ScrolledText(self.top, width=50, height=6,font=("微软雅黑",9))
        #self.Text2 = Entry(self.top, textvariable=self.data_result, font=('微软雅黑',9))
        self.Text2.place(relx=0.039, rely=0.44)


class Application(Application_ui):
    #这个类实现具体的事件处理回调函数。界面生成代码在Application_ui中。
    def __init__(self, master=None):
        Application_ui.__init__(self, master)

    def doupload(self, event=None):
        #TODO, Please finish the function here!
        pass

    def dotrans(self, event=None):
        dataurl = self.data_url.get()
        
        imgname = mytool.download_img(dataurl,"")
        mytool.dops_toweb()
        imgpath = mytool.psresult+imgname
        mytool.tryfile(imgpath)
        result = mytool.dobase64(imgpath)
        mytool.end(imgname)

        self.Text2.insert(END,result)

if __name__ == "__main__":
    top = Tk()
    Application(top).mainloop()
    try: top.destroy()
    except: pass

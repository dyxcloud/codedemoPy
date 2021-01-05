from pywinauto.application import Application

def open_notepad():
    '''打开计算器'''
    app = Application(backend="uia").start("notepad.exe")

def browser360():
    '''操作360极速浏览器'''
    app = Application(backend="uia").connect(process=22324)
    #w = app.window(title="")
    w = app.top_window()
    w.type_keys("^l")
    w.type_keys("www.baidu.com")
    w.type_keys("{ENTER}")
    print("done")

def ps():
    '''操作photoshop'''
    app = Application().connect(class_name="Photoshop",title="Adobe Photoshop CC 2019")
    win = app.top_window()
    win.type_keys("^o")
    print("done!")

#启动
ps()
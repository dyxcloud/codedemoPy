from pywinauto.application import Application

def ps():
    '''操作photoshop'''
    app = Application().connect(class_name="Photoshop",title="Adobe Photoshop CC 2019")
    win = app.top_window()
    win.type_keys("^o")
    print("done!")
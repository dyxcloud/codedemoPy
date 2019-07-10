from pywinauto.application import Application

# 打开计算器
# app = Application(backend="uia").start("notepad.exe")

#操作360极速浏览器
app = Application(backend="uia").connect(process=22324)
#w = app.window(title="")
w = app.top_window()
w.type_keys("^l")
w.type_keys("www.baidu.com")
w.type_keys("{ENTER}")
print("done")

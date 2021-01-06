import tkinter.messagebox

title = '提示'
msg = '要执行此操作吗'

root = tkinter.Tk()
root.title('GUI')  # 标题
root.geometry('8x6')  # 窗体大小
root.resizable(False, False)  # 固定窗体
root.after(2000, root.destroy)

a = tkinter.messagebox.askyesno(title, msg)
print(a)

import tkinter.messagebox

root = tkinter.Tk()
root.title('GUI')  # 标题
root.geometry('8x6')  # 窗体大小
root.resizable(False, False)  # 固定窗体
wait_time_sec = 20
root.after(wait_time_sec * 1000, root.destroy)
result = tkinter.messagebox.askretrycancel("提示", "检测到持续低网速,{}秒后将自动关机,点击重试取消关机".format(wait_time_sec))

import psutil
import time
import tkinter.messagebox
from collections import deque
import winsound


class SpeedChecker:
    sep = None  # 每秒间隔
    net_card = None  # 网卡名称
    target = None  # 网速阈值
    deque = None  # 速度缓存

    def __init__(self, sep=3, net_card='以太网', target=100.00, time_min=5):
        """
        构造函数
        :param sep: 检测间隔 秒
        :param net_card: 网卡名称
        :param target: 关机阈值 kB/s
        :param time_min: 持续时长 分钟
        """
        self.sep = sep
        self.net_card = net_card
        self.target = target
        q_len = int(time_min * (60 / sep))
        self.deque = deque(maxlen=q_len)

    def _get_speed(self):
        s1 = psutil.net_io_counters(pernic=True)[self.net_card]
        time.sleep(1)
        s2 = psutil.net_io_counters(pernic=True)[self.net_card]
        result = s2.bytes_recv - s1.bytes_recv
        # 除法结果保留两位小数
        result = result / 1024
        print("{:.2f}".format(result) + 'kB/s')
        return result

    @staticmethod
    def _do_shutdown():
        """弹出确认对话框, 并倒计时进行关机"""
        winsound.PlaySound('SystemExit', winsound.SND_ALIAS)

        print('关机啦')
        is_go_on = False
        return is_go_on

    @staticmethod
    def _show_message():
        """
        弹出关机提示框
        :return: True不关机 False执行关机
        """
        root = tkinter.Tk()
        root.title('GUI')  # 标题
        root.geometry('8x6')  # 窗体大小
        root.resizable(False, False)  # 固定窗体
        wait_time_sec = 20
        root.after(wait_time_sec * 1000, root.destroy)
        result = tkinter.messagebox.askretrycancel("提示", "检测到持续低网速,{}秒后将自动关机,点击重试取消关机".format(wait_time_sec))
        return result

    def run_check(self):
        """执行监控"""
        while True:
            time.sleep(self.sep - 1)
            s = self._get_speed()
            # 出现大于阈值的就清空队列
            if s > self.target and len(self.deque) > 0:
                self.deque.clear()
                continue
            self.deque.append(s)
            # 队列满了, 触发关机
            if len(self.deque) == self.deque.maxlen:
                is_go_on = self._do_shutdown()
                if is_go_on:
                    self.deque.clear()
                else:
                    break


if __name__ == "__main__":
    checker = SpeedChecker(sep=3, target=100.00, time_min=5)
    # checker.run_check()
    print('done~')

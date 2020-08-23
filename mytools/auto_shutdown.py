import psutil
import time
from collections import deque
import winsound


class speed_checker:

    sep = 3  # 每秒间隔
    net_card = '以太网'  # 网卡名称
    target = 100.00  # 网速阈值
    deque = deque(maxlen=int(1*(60/sep)))  # 速度缓存

    def __init__(self, sep=3, net_card='以太网', target=100.00):
        self.sep = sep
        self.net_card = net_card
        self.target = target

    def _get_speed(self):
        s1 = psutil.net_io_counters(pernic=True)[self.net_card]
        time.sleep(1)
        s2 = psutil.net_io_counters(pernic=True)[self.net_card]
        result = s2.bytes_recv - s1.bytes_recv
        # 除法结果保留两位小数
        result = result / 1024
        print("{:.2f}".format(result)+'kB/s')
        return result

    def _do_shutdown(self):
        '''弹出确认对话框, 并倒计时进行关机'''
        winsound.PlaySound('SystemExit', winsound.SND_ALIAS)
        
        print('关机啦')
        is_go_on = False
        return is_go_on

    def run_check(self):
        '''执行监控'''
        while True:
            time.sleep(self.sep-1)
            s = self._get_speed()
            self.deque.append(s)
            if s < self.target and len(self.deque) == self.deque.maxlen:
                need_shutdown = True
                for x in self.deque:
                    if x > self.target:
                        need_shutdown = False
                        break
                if need_shutdown:
                    is_go_on = self._do_shutdown()
                    if is_go_on:
                        self.deque.clear
                    else:
                        break


if __name__ == "__main__":
    checker = speed_checker()
    checker.run_check()
    print('done~')

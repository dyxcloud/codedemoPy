import psutil
import time
from collections import deque
import winsound


class speed_checker:

    sep = None  # 每秒间隔
    net_card = None  # 网卡名称
    target = None  # 网速阈值
    deque = None  # 速度缓存

    def __init__(self, sep=3, net_card='以太网', target=100.00, time = 5):
        self.sep = sep
        self.net_card = net_card
        self.target = target
        qlen = int( time * ( 60 / sep ))
        self.deque = deque(maxlen=qlen)

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
            #出现大于阈值的就清空队列
            if s > self.target and len(self.deque) > 0:
                self.deque.clear()
                continue
            self.deque.append(s)
            #队列满了, 触发关机
            if len(self.deque) == self.deque.maxlen:
                is_go_on = self._do_shutdown()
                if is_go_on:
                    self.deque.clear()
                else:
                    break


if __name__ == "__main__":
    checker = speed_checker(sep=3, target=100.00, time = 5)
    checker.run_check()
    print('done~')

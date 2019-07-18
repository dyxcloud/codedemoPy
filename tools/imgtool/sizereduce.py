import os
import time

#from tools.imgtool import pscontrol

def _tryfile(filepath):
    '''自旋10秒,判断文件是否导出完毕
    供ps生成, 需要改进
    '''
    start = time.time()
    long = 10.0

    # isnot_exist = True
    # while time.time()-start<long and isnot_exist:
    #     isnot_exist = not os.path.exists(filepath)

    time.sleep(1)

    # isnot_exist = True
    # while time.time()-start<long and isnot_exist:
    #     size = not os.path.getsize(filepath)
    #     if size>10 :
    #         isnot_exist = False

    # isnot_exist = True
    # while time.time()-start<long and isnot_exist:
    #     try:
    #         f =open(filepath,"ab")
    #         f.close()
    #         isnot_exist = False
    #     except IOError:
    #         print("File is not accessible")


def compression(source, result):
    #暂不使用ps
    #pscontrol.dops_toweb()
    #_tryfile(result_path)
    #TODO 类型判断
    _towebp(source,result)

def _towebp(source, result):
    if os.path.splitext(source)[1]==".gif":
        commond="gif2webp.exe -mixed -q 30 -m 6 -mt \"{}\" -o \"{}\"".format(source,result)
    else:
        commond = "cwebp.exe -q 30 -m 6 -mt -size 70000 \"{}\" -o \"{}\"".format(source,result)
        # commond = "cwebp.exe -q 30 -m 6 -mt {} -o {}".format(source,result)
    os.system(commond)

def _topng(source, result):
    #使用pngquant转换,图源只支持png
    if os.path.splitext(source)[1]==".png":
        commond="pngquant.exe --force --strip --ordered --speed=1 --quality=20-60 \"{}\" -o \"{}\"".format(source,result)
    os.system(commond)

if __name__ == "__main__":
    s = r"D:\Download\timg2.png"
    r = r"D:\Download\timg2new.png"
    _topng(s,r)
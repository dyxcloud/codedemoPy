import os
import math
import winsound
from subprocess import run

from PIL import Image
from mytools.bango import _is_img



def get_size(imgpath):
    img = Image.open(imgpath)
    return img.size #(宽,高)

command = 'C:\Programs\waifu2x-caffe\waifu2x-caffe-cui.exe \
-e jpg -q 100 -m auto_scale -n 1 -s {scale} -b 18 -c 64 -p cudnn -t 0 \
-i {imgpath}'
def _waifu2x(imgpath,scale):
    # print(command.format(imgpath=imgpath,scale=scale))
    run(command.format(imgpath=imgpath,scale=scale),shell=True)

def dotask(path):
    #横向的大于2560 1440
    #纵向的大于1600 2560
    l = []
    for root, dirs, files in os.walk(path):
        for file in files:
            target = os.path.join(root,file)
            if _is_img(target):
                l.append(target)
            else:
                print("found other type file: "+target)

    count_all = len(l)
    for index,target in enumerate(l):
        sizes = get_size(target)
        print('>>{}/{}\tget img[{}] size{}'.format(index+1,count_all,target,sizes))
        width,hight = sizes[0],sizes[1]
        scale = None
        if width>hight:
            scale = max(math.ceil(2560/width),math.ceil(1440/hight))
        elif width<hight:
            scale = max(math.ceil(1600/width),math.ceil(2560/hight))
        else:
            scale = math.ceil(2560/width)
        if scale>1:
            _waifu2x(target,scale/1)
    winsound.PlaySound('SystemExit', winsound.SND_ALIAS)


if __name__ == "__main__":
    dotask(r'D:\Download\p\图片任务组_20191219_22271')
    # _waifu2x(r'D:\Download\test\43287671_p0.jpg',3.0)
    
    print("done~")
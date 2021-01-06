import os
import math
import winsound
from subprocess import run

from PIL import Image
from src.mytools.bango import _is_img


def get_size(imgpath):
    img = Image.open(imgpath)
    return img.size  # (宽,高)


command = "C:\Programs\waifu2x-caffe\waifu2x-caffe-cui.exe \
-e jpg -q 100 -m auto_scale -n 1 -s {scale} -b 18 -c 64 -p cudnn -t 0 \
-i {img_path}"


def _waifu2x(path, scale):
    # print(command.format(img_path=path,scale=scale))
    run(command.format(img_path=path, scale=scale), shell=True)


def do_task(path):
    # 横向的大于2560 1440
    # 纵向的大于1600 2560
    img_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            target = os.path.join(root, file)
            if _is_img(target):
                img_list.append(target)
            else:
                print("found other type file: " + target)

    count_all = len(img_list)
    for index, target in enumerate(img_list):
        sizes = get_size(target)
        print('>>{}/{}\tget img[{}] size{}'.format(index + 1, count_all, target, sizes))
        width, height = sizes[0], sizes[1]
        if width > height:
            scale = max(math.ceil(2560 / width), math.ceil(1440 / height))
        elif width < height:
            scale = max(math.ceil(1600 / width), math.ceil(2560 / height))
        else:
            scale = math.ceil(2560 / width)
        if scale > 1:
            _waifu2x(target, scale / 1)
    winsound.PlaySound('SystemExit', winsound.SND_ALIAS)


if __name__ == "__main__":
    # do_task(r'D:\Download\p\图片任务组_20191219_2227')
    _waifu2x(r'D:\Download\61215438_p0.png', 2.0)

    print("done~")

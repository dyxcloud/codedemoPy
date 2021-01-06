import os
from PIL import Image

"""对手机漫画截图进行截取, 去除黑屏部分, 获取中间图像部分"""


def _get_size(img_path):
    img = Image.open(img_path)
    return img.size  # (宽,高)


def _get_xy(source_path, result_path):
    im = Image.open(source_path)

    # 二值化
    threshold_low = 45
    threshold = 50
    table = []
    for x in range(256):
        if x < threshold_low:
            table.append(1)
        elif x < threshold:
            table.append(0)
        else:
            table.append(1)
    im = im.convert("L").point(table, '1')
    # im.save(result_path)

    width, height = im.size
    x1, y1 = 0, 0
    x2, y2 = width - 1, height - 1
    # 判断图片空白方向
    is_vertical = any([im.getpixel((x, height - 1)) for x in range(500, width)])
    print("垂直图片" if is_vertical else "水平图片")
    # 边界计算
    find_sep = False
    if not is_vertical:  # 空白水平
        x1, x2 = 0, width - 1
        for y in range(90, height):
            has = any([im.getpixel((x, y)) for x in range(500, width)])  # 去掉左下角区域
            if (not find_sep) and (not has):
                # 上留白
                continue
            elif not find_sep:
                # 上分界
                y1 = y
                find_sep = True
            elif find_sep and (not has):
                # 下分界
                y2 = y
                break
    else:  # 空白垂直
        y1, y2 = 90, height - 1
        for x in range(0, width):
            has = any([im.getpixel((x, y)) for y in range(90, 2190)])  # 去掉左下角区域
            if (not find_sep) and (not has):
                # 左留白
                continue
            elif not find_sep:
                # 左分界
                x1 = x
                find_sep = True
            elif find_sep and (not has):
                # 右分界
                x2 = x
                break

    return x1, y1, x2, y2


def trans_img(source_path, result_path):
    im = Image.open(source_path)
    width, height = im.size
    print(f"geted {os.path.basename(source_path)} {width}*{height}")

    x1, y1, x2, y2 = _get_xy(source_path, result_path)
    print(f"geted ({x1},{y1}) ({x2},{y2})")
    # 分割
    im = im.crop((x1, y1, x2 + 1, y2 + 1))
    im.save(result_path)


def transFolder(path):
    for file in os.listdir(path):
        r = os.path.join(path, file)
        target_dir = path + "result/"
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        target = os.path.join(target_dir, file)
        # print(r)
        # print(target)
        trans_img(r, target)


if __name__ == "__main__":
    # transImg(r"D:\Download\picacg\Screenshot_2020-02-17-13-53-22-240_com.picacomic.fregata.jpg"
    # ,r"D:\Download\result\a.png")
    transFolder(r"D:\Download\picacg/")
    print("done~")

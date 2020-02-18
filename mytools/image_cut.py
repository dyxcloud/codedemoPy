import os
from PIL import Image

'''对手机漫画截图进行截取, 去除黑屏部分, 获取中间图像部分'''


def _get_size(imgpath):
    img = Image.open(imgpath)
    return img.size  # (宽,高)



def _getxy(sourcepath, resultpath):
    im = Image.open(sourcepath)

    #二值化
    threshold_low = 45
    threshold = 50
    table = []
    for i in range(256):
        if i < threshold_low:
            table.append(1)
        elif i < threshold:
            table.append(0)
        else:
            table.append(1)
    im = im.convert("L").point(table, '1')
    # im.save(resultpath)

    width, height = im.size
    x1, y1 = 0, 0
    x2, y2 = width-1, height-1
    #判断图片空白方向
    r = im.getpixel((int(width/2), height-1))
    isVertical = (r == 255)
    #边界计算
    findSep = False
    if not isVertical:#空白水平
        x1,x2 = 0,width-1
        for i in range(90, height):
            has = any([im.getpixel((x,i)) for x in range(440,width)]) #去掉左下角区域
            if (not findSep) and (not has):
                #上留白
                continue
            elif not findSep:
                #上分界
                y1 = i
                findSep = True
            elif (findSep) and (not has):
                #下分界
                y2 = i
                break
    else:#空白垂直
        y1,y2 = 90,height-1
        for i in range(0, width):
            has = any([im.getpixel((i,y)) for y in range(90,2190)]) #去掉左下角区域
            if (not findSep) and (not has):
                #左留白
                continue
            elif not findSep:
                #左分界
                x1 = i
                findSep = True
            elif (findSep) and (not has):
                #右分界
                x2 = i
                break
    
    return x1, y1, x2, y2


def transImg(sourcepath, resultpath):
    im = Image.open(sourcepath)
    width, heght = im.size
    print(f"geted {os.path.basename(sourcepath)} {width}*{heght}")

    x1, y1, x2, y2 = _getxy(sourcepath, resultpath)
    print(f"geted ({x1},{y1}) ({x2},{y2})")
    #分割
    im = im.crop((x1, y1, x2, y2))
    im.save(resultpath)


def transFolder(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            r = os.path.join(root, file)
            target = os.path.join(root, "result/", file)
            # print(r)
            # print(target)
            transImg(r, target)


if __name__ == "__main__":
    # transImg(r"D:\Download\picacg\Screenshot_2020-02-17-13-53-05-351_com.picacomic.fregata.jpg"
    # ,r"D:\Download\picacg\result\a.png")
    transFolder(r"D:\Download\picacg")
    print("done~")

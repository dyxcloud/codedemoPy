import os
import urllib.request
from pywinauto.application import Application
import time
from base64 import b64encode

psworkspace = r"C:/WorkSpace/photoshop/"
psresult = psworkspace + "result/"

def download_img(img_url, api_token):
    '''下载图片'''
    #TODO 去除url参数
    header = {"Authorization": "Bearer " + api_token} # 设置http header
    request = urllib.request.Request(img_url, headers=header)
    try:
        response = urllib.request.urlopen(request)
        img_name = os.path.basename(img_url)
        filename = psworkspace+ img_name
        if (response.getcode() == 200):
            with open(filename, "wb") as f:
                f.write(response.read()) # 将内容写入图片
            return img_name
    except:
        return "failed"

def dops_toweb():
    '''操作photoshop'''
    app = Application().connect(class_name="Photoshop",title="Adobe Photoshop CC 2019")
    win = app.top_window()
    win.type_keys("%f")
    win.type_keys("ub")
    win.type_keys("{ENTER}")
    win.minimize()
    #print("done!")

def tryfile(filepath):
    '''自旋10秒,判断文件是否导出完毕'''
    time.sleep(0.5)
    start = time.time()
    long = 10.0

    isnot_exist = True
    while time.time()-start<long and isnot_exist:
        isnot_exist = not os.path.exists(filepath)

    isnot_exist = True
    while time.time()-start<long and isnot_exist:
        size = not os.path.getsize(filepath)
        if size>10 :
            isnot_exist = False

    isnot_exist = True
    while time.time()-start<long and isnot_exist:
        try:
            f =open(filepath,"ab")
            f.close()
            isnot_exist = False
        except IOError:
            print("File is not accessible")

def dobase64(filename):
    '''本地图片转base64'''
    with open(filename,"rb") as f:#转为二进制格式
        data = b64encode(f.read())#使用base64进行加密
        return _base64_getheader(filename)+data.decode()

def _base64_getheader(filename):
    '''获取base64头'''
    ex = os.path.splitext(filename)[1]
    switch = {
        '.gif':"data:image/gif;base64,",
        '.png':"data:image/png;base64,",
        '.jpg':"data:image/jpeg;base64,",
        '.ico':"data:image/x-icon;base64,"
    }
    return switch[ex]

def end(imgname):
    '''删除本地结果'''
    result = psresult+imgname
    source = psworkspace+imgname
    os.remove(result)
    os.remove(source)

#program
'''
基本流程:
1. url转本地图片
2. 本地图片压缩
3. 图片转base64
4. gui
'''
if __name__ == "__main__":
    imgname = download_img("https://cdn.v2ex.com/avatar/b8e4/befb/18748_large.png",'')
    dops_toweb()
    imgpath = psresult+imgname
    tryfile(imgpath)
    result = dobase64(imgpath)
    end(imgname)
    print(result)
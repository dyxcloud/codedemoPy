import os

from base64 import b64encode

from tools.imgtool import sizereduce
from tools.imgtool import downloader

psworkspace = r"C:/WorkSpace/photoshop/"
psresult = psworkspace + "result/"
#初始化工作目录
if not os.path.exists(psresult):
    os.mkdir(psresult)
base64headers = {
    '.gif': "data:image/gif;base64,",
    '.png': "data:image/png;base64,",
    '.jpg': "data:image/jpeg;base64,",
    '.ico': "data:image/x-icon;base64,",
    '.webp': "data:image/webp;base64,"
}

def filename_change(filename,ex):
    '''更改后缀名,ex=png'''
    name = os.path.splitext(filename)[0]
    return name+"."+ex

def dobase64_with_bytes(bytes,filename):
    data = b64encode(bytes)
    return _base64_getheader(filename)+data.decode()

def dobase64(filename):
    '''本地图片转base64'''
    with open(filename, "rb") as f:  # 转为二进制格式
        data = b64encode(f.read())  # 使用base64进行加密
        return _base64_getheader(filename)+data.decode()

def _base64_getheader(filename):
    '''获取base64头'''
    ex = os.path.splitext(filename)[1]
    return base64headers[ex]


def work_url(url):
    response,imgname = downloader.get_response_imgname(url)
    result_line = dobase64_with_bytes(response.read(),imgname)
    return result_line

def work_url_compression(url):
    imgname = downloader.download_img(url)
    source_path = psworkspace+imgname
    result_path = psresult+filename_change(imgname,"webp")
    sizereduce.compression(source_path,result_path)
    result_line = dobase64(result_path)
    os.remove(source_path)
    os.remove(result_path)
    return result_line


def work_file(filepath):
    pass


def work_file_compression(filepath):
    pass


# program
'''
基本流程:
1. url转本地图片
2. 本地图片压缩
3. 图片转base64
4. gui
'''
if __name__ == "__main__":
    #TODO 自动根据尺寸判断是否压缩
    #TODO png模式 webp模式 gif全转webp
    re = work_url("https://images2017.cnblogs.com/blog/828214/201710/828214-20171007083032318-501050226.png")
    print(len(re))

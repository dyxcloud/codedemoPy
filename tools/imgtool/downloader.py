import os
import urllib.request

from tools.imgtool import mytool

content_types = {
    'image/jpeg':'.jpg',
    'application/x-jpg':'.jpg',
    'image/gif':'.gif',
    'image/png':'.png',
    'application/x-png':'.png',
    'image/x-icon':'.ico',
    'application/x-ico':'.ico'
}

def _get_name_from_url(url,contenttype):
    #文件名
    end = url.index("?")-1
    name = url[:end]
    name = name.rpartition("/")[2]
    # 根据content type 判断文件类型
    if contenttype in content_types:
        ex = content_types[contenttype]
    else:
        for type in set(content_types.values()):
            if type in url:
                ex = type
                break
    return name+ex

def get_response_imgname(img_url):
    request = urllib.request.Request(img_url)
    response = urllib.request.urlopen(request)
    if (response.getcode() == 200):
        contenttype = response.headers['Content-Type']
        img_name = _get_name_from_url(img_url,contenttype)
        return response,img_name
    else:
        print("request fail!")
        return None,None

def download_img(img_url):
    '''下载图片'''
    response,img_name = get_response_imgname(img_url)
    filename = mytool.psworkspace + img_name
    with open(filename, "wb") as f:
        f.write(response.read())
    return img_name


if __name__ == "__main__":
    name = _get_name_from_url("https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1563513452305&di=e06b6b2dbf1d56c4fc82c709a4705671&imgtype=0&src=http%3A%2F%2Fimg3.redocn.com%2Ftupian%2F20150210%2Flvsejiantouppttubiao_3854182.jpg","")
    print(name)
    # print(content_types.values)
    
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
    'application/x-ico':'.ico',
}

def get_response_imgname(img_url):
    request = urllib.request.Request(img_url)
    response = urllib.request.urlopen(request)
    if (response.getcode() == 200):
        # 根据content type 判断文件类型
        contenttype = response.headers['Content-Type']
        if contenttype in content_types:
            img_name = os.path.basename(img_url)+content_types[contenttype]
        else:
            img_name = os.path.basename(img_url)
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
    download_img("https://images2017.cnblogs.com/blog/828214/201710/828214-20171007083032318-501050226.png")
    
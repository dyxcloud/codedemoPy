#通过文件名获取番号


import re
import glob
import os
from mytools.get_tag_by_av import get_jav,get_javbus


lreg = [re.compile(r"^[a-zA-Z]+\d*[-_][a-zA-Z]*\d{2,} ")
    ,re.compile(r"^[a-zA-Z]+\d+[a-zA-Z]+[-_]\d{2,} ") #S2M-019
    ,re.compile(r"^\d+[_-]\d{2,} ") #061315_01
    ,re.compile(r"^\d+[_-][a-zA-Z]{3,} ") #150123-YUME
    ,re.compile(r"^\d+[a-zA-Z]+[_-]\d{2,} ") #259LUXU-891
    ,re.compile(r"^[a-zA-Z]+\d{2,} ") #CZ021
]
def get_bango(filename):
    '''获取番号'''
    for reg in lreg:
        match_bango = re.search(reg, filename)
        if match_bango:
            return match_bango.group()
    return None

def list_file_name(filepath):
    '''获取目录下所有全路径文件名'''
    result = []
    for root, dirs, files in os.walk(filepath):
        for file in files:
            r = os.path.join(root, file)
            if _is_video(r) and _not_skip_flie(r):
                result.append(r)
    return result

lvideo = {'avi','flv','mkv','mp4','rmvb','rm','wmv','divx'}
def _is_video(filename):
    ex = filename[filename.rindex('.')+1:]
    return ex.lower() in lvideo

limg = {'jpg','jpeg','png','webp','bmp'}
def _is_img(filename):
    ex = filename[filename.rindex('.')+1:]
    return ex.lower() in limg

lblack = {'scu','kizunanosora','S-Cute','ps7','Siberian Mouse','shemaleJP','foreign','短片'
,'19id'}
def _not_skip_flie(filename):
    for b in lblack:
        if filename.find(b)>=0:
            return False
    return True


re_img = re.compile(r"\d+")
def reset_image(mypath):
    '''TODO 获取 视频和对应封面 列出没有被匹配的图片'''
    for root, dirs, files in os.walk(mypath):
        for file in files:
            if not _is_img(file):
                continue
            match = re.search(re_img,file)
            if match:
                if not _is_finded(match.group(),root):
                    print("not video: "+file)
            else:
                print("not key "+file)

def _is_finded(num,path):
    # print("start find num={}".format(num))
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path,file)) and _is_video(file) and file.find(num)>=0:
            return True
    return False

def print_tag_by_dir(mypath):
    for s in list_file_name(mypath):
        bango = get_bango(os.path.basename(s))
        if bango:
            print(bango)
            print(get_jav(bango))
            # print(get_javbus(bango))
        else:
            print("error get bango: " +s)
    
def print_tag_by_url():
    urls = ['https://www.javbus.com/012617-359',
'http://www.r40z.com/cn/?v=javliit4r4',
'http://www.r40z.com/cn/?v=javliiyl6a',
'http://www.r40z.com/cn/?v=javlipi3qu',
'https://www.javbus.com/Jukujo-2610',
'http://www.r40z.com/cn/?v=javli4tiyy']
    for url in urls:
        print(url)
        if url.find('javbus')<0:
            print(get_jav(url,True))
        else:
            print(get_javbus(url,True))


if __name__ == "__main__":
    mypath = r"D:\Games\project\hentai\Shemale"
    # print_tag_by_dir(mypath)

    print_tag_by_url()

    # mypath = r"D:\Games\project"
    # reset_image(mypath)

    # print(_is_finded('xrw','565',r'D:\Games\project\hentai\其他'))

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

lvideo = {'avi','flv','mkv','mp4','rmvb','wmv'}
def _is_video(filename):
    ex = filename[filename.rindex('.')+1:]
    return ex.lower() in lvideo

lblack = {'scu','kizunanosora','S-Cute','ps7','Siberian Mouse','shemaleJP','foreign','短片'
,'19id'}
def _not_skip_flie(filename):
    for b in lblack:
        if filename.find(b)>=0:
            return False
    return True

#TODO 获取 视频和对应封面 列出没有被匹配的图片

if __name__ == "__main__":
    mypath = r"D:\Games\project\hentai\COSAV\新建文件夹"
    for s in list_file_name(mypath):
        bango = get_bango(os.path.basename(s))
        if bango:
            print(bango)
            print(get_jav(bango))
            # print(get_javbus(bango))
        else:
            print("error get bango: " +s)
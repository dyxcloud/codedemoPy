import re
import glob
import os

mypath = "D:/Games/project/hentai/"

def get_number(filename):
    '''获取番号'''
    # return re.search("[a-zA-Z]+-?\d+[a-zA-Z]?",filename).group()
    rr = re.search("[a-zA-Z]+-?\d+",filename)
    if(rr):
        return rr.group()
    else:
        return ""

def get_all_filename(filepath):
    '''获取目录下所有文件名'''
    result = []
    list = os.walk(filepath)
    for path,dir_list,file_list in list:  
        for file_name in file_list:  
            r = os.path.join(path, file_name)
            r = os.path.basename(r)
            result.append(r)
    return result
    
#launch
for m in get_all_filename(mypath):
        print(m+"===="+get_number(m))

# print(get_number("ppt-018A.mkv"))
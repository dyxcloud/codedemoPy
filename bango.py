import re
import glob
import os

def get_bango(filename):
    '''获取番号'''
    # return re.search("[a-zA-Z]+-?/d+[a-zA-Z]?",filename).group()
    rr = re.search("[a-zA-Z]+-?\\d+", filename)
    if(rr):
        return rr.group()
    else:
        return "error when find = "+filename

def list_file_name(filepath):
    '''获取目录下所有全路径文件名'''
    result = []
    for root, dirs, files in os.walk(filepath):
        for file in files:
            r = os.path.join(root, file)
            result.append(r)
    return result

# launch
mypath = "D:\\localFile\\h"
for s in list_file_name(mypath):
    print(get_bango(os.path.basename(s)))
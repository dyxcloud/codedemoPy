import re
import glob
import os

mypath = "D:/localFile/h/"

def get_number(filename):
    return re.search("[a-zA-Z]+-?\d+",filename).group()

def get_all_filename(filepath):
    result = []
    list = os.walk(filepath)
    for path,dir_list,file_list in list:  
        for file_name in file_list:  
            r = os.path.join(path, file_name)
            result.append(r)
    return result
    
for m in get_all_filename(mypath):
        print(get_number(m))

import re
import glob
import os

mypath = "D:/localFile/h/"

def get_number(filename):
    return re.search("[a-zA-Z]+-?\d+[a-zA-Z]?",filename).group()

def get_all_filename(filepath):
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
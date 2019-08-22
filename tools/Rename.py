import os
import shutil

def work_subdir(path):
    '''遍历路径下的子文件夹'''
    for root,dirs,files in os.walk(path):
        for dir in dirs:
            dir1 = root+"/"+dir+"/" #vol文件夹
            for root1,dirs1,files1 in os.walk(dir1):
                for file in files1:
                    if(str(file).endswith(".jpg")):
                        print(dir1+file+" to "+dir1+dir+".jpg")
                        os.rename(dir1+file,dir1+dir+".jpg")

def work_subfile(path):
    '''遍历路径下的文件'''
    for root,dirs,files in os.walk(path):
        for file in files:
            dd = file[0:3]
            s = root+file
            d = root+dd+"/"
            print("move file: {} to dir: {}".format(s,d))
            if not os.path.exists(d):
                os.mkdir(d)
            shutil.move(root+file,root+dd+"/")


if __name__ == "__main__":
    path=r"D:\Download\深红累之渊/"
    work_subfile(path)
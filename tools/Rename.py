import os

path="D:\OneDrive - business\Video\A+\DARLING in the FRANXX\Scans"

for root,dirs,files in os.walk(path):
    for dir in dirs:
        dir1 = root+"/"+dir+"/" #vol文件夹
        for root1,dirs1,files1 in os.walk(dir1):
            for file in files1:
                if(str(file).endswith(".jpg")):
                    print(dir1+file+" to "+dir1+dir+".jpg")
                    os.rename(dir1+file,dir1+dir+".jpg")
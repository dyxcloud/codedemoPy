import re

#https://www.pixiv.net/ajax/illust/61791949/pages


re_pid = re.compile(r'(\d{8,})')
re_pno = re.compile(r'([pP]\d{1,2})')
def getPID(filename):
    pid=None
    pno=None
    mpid = re.search(re_pid,filename)
    if mpid:
        pid = mpid.group(1)
    mpno = re.search(re_pno,filename)
    if mpno:
        pno = mpno.group(1)
    return pid,pno

def _test_getPID():
    print(getPID("61791949_p0.webp"))
    print(getPID("62025919_シロクマA＠2日目Q-04b]週刊熊の穴#33 2B メインテナンス中P0_00000.webp"))
    print(getPID("62029906_はれんちとめこ]ﾂｲｯﾀｰ落書きまとめP1_00000.webp"))
    print(getPID("66078530_p2.webp"))
    print(getPID("66078530.webp"))

if __name__ == "__main__":
    _test_getPID()
    pass
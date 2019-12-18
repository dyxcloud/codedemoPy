import re
from urllib import request
import json


def getFileNameList(path):
    #TODO
    pass


re_pid = re.compile(r'(\d{8,})')
re_pno = re.compile(r'(?<=[pP])(\d{1,2})')
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


#https://www.pixiv.net/ajax/illust/61791949/pages
httpproxy_handler = request.ProxyHandler({'https':'127.0.0.1:25378'})
opener = request.build_opener(httpproxy_handler)
request.install_opener(opener)
def getJson(pid):
    url = "https://www.pixiv.net/ajax/illust/"+pid+"/pages"
    req = request.Request(url)
    req.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36")
    with request.urlopen(req) as f:
        if f.status == 200:
            data = f.read()
            return data.decode('utf-8')
        else:
            return None

def getImgList(pid,pno):
    data = getJson(pid)
    if data is not None:
        jdata = json.loads(data)
        if jdata['error'] is not 'true':
            body = jdata['body']
            if len(body) is not 0:
                if pno is not None:
                    return [body[pno]['urls']['original']]
                else:
                    return [x['urls']['original'] for x in body]
    return None

def program():
    
    pass

if __name__ == "__main__":
    #print(getImgList("61791949",None))
    _test_getPID()
    pass
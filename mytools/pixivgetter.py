import os
import re
from urllib import request
import json


def getFileNameList(path):
    return [filename for filename in os.listdir(path)]


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
        pno = int(pno)
    return pid,pno

def _test_getPID():
    print(getPID("61791949_p0.webp"))
    print(getPID("62025919_シロクマA＠2日目Q-04b]週刊熊の穴#33 2B メインテナンス中P0_00000.webp"))
    print(getPID("62029906_はれんちとめこ]ﾂｲｯﾀｰ落書きまとめP1_00000.webp"))
    print(getPID("66078530_p2.webp"))
    print(getPID("66078531.webp"))


#https://www.pixiv.net/ajax/illust/61791949/pages
httpproxy_handler = request.ProxyHandler({'https':'127.0.0.1:25378'})
opener = request.build_opener(httpproxy_handler)
request.install_opener(opener)
def _getJson(pid):
    url = "https://www.pixiv.net/ajax/illust/"+pid+"/pages"
    print("url:{}".format(url))
    req = request.Request(url)
    req.add_header('accept-language','zh-CN,zh;q=0.9')
    req.add_header('cache-control','no-cache')
    req.add_header('pragma','no-cache')
    req.add_header('referer','https://www.pixiv.net/')
    req.add_header('cookie',cookie)
    req.add_header("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")
    with request.urlopen(req) as f:
        if f.status == 200:
            data = f.read()
            return data.decode('utf-8')
        else:
            return None

def getImgList(pid,pno):
    data = _getJson(pid)
    if data is not None:
        jdata = json.loads(data)
        if jdata['error'] is not 'true':
            body = jdata['body']
            if len(body) is not 0:
                if pno is not None:
                    if pno<len(body): return [body[pno]['urls']['original']]
                else:
                    return [x['urls']['original'] for x in body]
    return None

def cleanText(filepath):
    if os.path.exists(filepath): os.remove(filepath)

def saveText(filepath,data):
    with open(filepath,'at') as f:
        f.write(data+'\n')

target = r"D:\Download\p"
resultfile = r"D:\Download\presult.txt"
errorfile = r"D:\Download\perror.txt"
cookie = 'first_visit_datetime_pc=2019-04-19+20%3A21%3A12; p_ab_id=5; p_ab_id_2=6; p_ab_d_id=553978108; yuid_b=QTIlAEQ; p_b_type=1; privacy_policy_agreement=1; login_bc=1; PHPSESSID=6001922_FXLI2MBFEKvBU8hvA3qvyRu3WBJvKk4v; device_token=7a4717d01537fa000404a6fe4cfbaf3f; c_type=26; a_type=0; b_type=1; tag_view_ranking=AG0hQxVDJ6~0xsDLqCEW6~CsU1y07-7D~Sbp1gmMeRy~UZootLOo57~_-agXPKuAQ~KN7uxuR89w~2EpPrOnc5S~yS_WrRrWFi~HBYFbIUAS8~UJAHVojA30~-IDD9G1jrk~gSkWaAUCID~-dlArdyvmu~npAXet7x_g~zBazw5YSRX~JvZxvIGtdk~T9AkOP6tYq~gV5ZWAcgjv~y8GNntYHsi~BU9SQkS-zU~tKWyFlqScc~K8esoIs2eW~6293srEnwa~xhUktaVjvC~1F9SMtTyiX~xZ6jtQjaj9'
def program():
    count_all,count_good,count_bad = 0,0,0
    cleanText(resultfile)
    cleanText(errorfile)
    namelist = getFileNameList(target)
    count_all = len(namelist)
    print("find {} images".format(count_all))
    for filename in namelist:
        isGood = False
        pid,pno = getPID(filename)
        if pid is not None:
            result = getImgList(pid,pno)
            if result is not None and len(result) is not 0:
                for r in result:
                    saveText(resultfile,r)
                    if not isGood: count_good+=1
                    isGood = True
        if not isGood:
            saveText(errorfile,filename)
            count_bad+=1
    print("done!")
    print("goodFile:{}\nbadfile:{}".format(count_good,count_bad))

if __name__ == "__main__":
    #print(getImgList("61791949",None))
    # list(map(print,getFileNameList(target)))
    program()
    print("done")
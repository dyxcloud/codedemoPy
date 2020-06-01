import os
import re
from urllib import request
from retrying import retry
import json
import sys


def getFileNameList(path):
    return os.listdir(path)


re_pid = re.compile(r'\d{8,}')
re_pno = re.compile(r'(?<=[pP])\d{1,2}')
def getPID(filename):
    '''解析文件名,获取pid'''
    pid,pno=None,None
    mpid = re.search(re_pid,filename)
    if mpid:
        pid = mpid.group()
    mpno = re.search(re_pno,filename)
    if mpno:
        pno = int(mpno.group())
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
@retry(stop_max_attempt_number=3,wait_random_min=1000, wait_random_max=3000)
def _getJson(pid):
    '''请求p站图片信息接口, 返回json'''
    url = "https://www.pixiv.net/ajax/illust/"+pid+"/pages"
    req = request.Request(url)
    req.add_header('accept-language','zh-CN,zh;q=0.9')
    req.add_header('cache-control','no-cache')
    req.add_header('pragma','no-cache')
    req.add_header('referer','https://www.pixiv.net/')
    req.add_header('cookie',cookie)
    req.add_header("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")
    with request.urlopen(req,timeout=10) as f:
        if f.status == 200:
            data = f.read()
            return data.decode('utf-8') 
    return None

def getImgList(pid,pno):
    '''返回pid所有图片列表,或者指定的no链接'''
    data = None
    try:
        data = _getJson(pid)
    except:
        print("Unexpected error:", sys.exc_info()[:2])
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
    iserror = filepath == errorfile
    with open(filepath,'at') as f:
        f.write(data)
        if iserror: f.write(' |')
        f.write('\n')

def program():
    '''扫描本地指定目录, 获取图片pid的原始url'''
    count_all,count_good,count_bad = 0,0,0
    cleanText(resultfile)
    cleanText(errorfile)
    namelist = getFileNameList(target)
    count_all = len(namelist)
    print("find {} images".format(count_all))
    for index,filename in enumerate(namelist):
        isGood = False
        pid,pno = getPID(filename)
        print(">>{}/{}\tpid:{}\tpno:{}".format(index+1,count_all,pid,pno))
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
    print("done!\nfind {} images\ngoodFile:{}\nbadfile:{}".format(count_all,count_good,count_bad))

target = "D:/file/Picture/ACG/P站/"
resultfile = "D:/Download/presult.txt"
errorfile = "D:/Download/perror.txt"
cookie = 'p_ab_id=7; p_ab_id_2=3; a_type=0; b_type=1; login_ever=yes; privacy_policy_agreement=1; first_visit_datetime_pc=2018-06-21+22%3A18%3A44; p_ab_d_id=2036277048; yuid_b=FFQJZAk; module_orders_mypage=%5B%7B%22name%22%3A%22sketch_live%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22tag_follow%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22recommended_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22everyone_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22following_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22mypixiv_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22fanbox%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22featured_tags%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22contests%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22user_events%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22sensei_courses%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22spotlight%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22booth_follow_items%22%2C%22visible%22%3Atrue%7D%5D; c_type=26; __cfduid=db81627975e528c2a39ebfef8e81b06c41586184985; login_bc=1; PHPSESSID=6001922_ntgV3y65n4hJo0EFWzykyUsAcHwrdaIN; device_token=5a0e2e1db42c7f699b77548e2e50c336; tag_view_ranking=0xsDLqCEW6~RTJMXD26Ak~6293srEnwa~qWFESUmfEs~Lt-oEicbBr~jH0uD88V6F~LVSDGaCAdn~BU9SQkS-zU~y8GNntYHsi~CrFcrMFJzz~xhUktaVjvC~KN7uxuR89w~RcahSSzeRf~-StjcwdYwv~tKWyFlqScc~uusOs0ipBx~LJo91uBPz4~D0nMcn6oGk~jk9IzfjZ6n~MM6RXH_rlN~X_1kwTzaXt~-98s6o2-Rp~kGYw4gQ11Z~Ie2c51_4Sp~EUwzYuPRbU~RySOhMndf4~JN2fNJ_Ue2~xZ6jtQjaj9~YUuqn7At7n~84R8mUJ19X~tzIoUMzCb7~zZZn32I7eS~jhuUT0OJva~qtVr8SCFs5~HY55MqmzzQ~ABWTvyMCOF~engSCj5XFq~8QDQMYtZHY~h9fEA3tOFb~5oPIfUbtd6~azESOjmQSV~UR3UZdHtim~i4Q_o7CyIB~59dAqNEUGJ~LLyDB5xskQ~rkLi5JvRDj~CiSz61UwrQ~1CWwi2xr7g~e6DJejypJg~K6fORPJca3~BtXd1-LPRH~uvBGOtCzqF~Bd2L9ZBE8q~KOnmT1ndWG~QaiOjmwQnI~-TeGk6mN86~EZQqoW9r8g~_pwIgrV8TB~D4hLr_YmAD~T40wdiG5yy~yPNaP3JSNF~-Pl_yN8N1A~X5Vyd3xoDs~JrbpHxlmCl~G-44hwuIPi~zsm1ECW5Wb~iFcW6hPGPU~KvAGITxIxH~9ODMAZ0ebV~1Xn1rApx2-~eVxus64GZU~hAaisbVESe~zIv0cf5VVk~mWkK54Tv3w~MO67n2Zm2e~65aiw_5Y72~-sp-9oh8uv~PHQDP-ccQD~ouQb1xvzoB~xYzU0doFjn~mzJgaDwBF5~SoxapNkN85~TcgCqYbydo~DADQycFGB0~JXmGXDx4tL~cbmDKjZf9z~jEoxuA2PIS~Hir4f1f8T_~ZTBAtZUDtQ~bcAbumoPKA~mHukPa9Swj~pnCQRVigpy~iWYAidoiGx~OgdypjrwdX~qcYo_5oqVP~rOnsP2Q5UN~BtlFaO8rDF~ePN3h1AXKX~MSNRmMUDgC~WQEYXrP9z0'

if __name__ == "__main__":
    # _test_getPID()
    print(getImgList("80316543",None))
    # list(map(print,getFileNameList(target)))
    # program()
    print("done")
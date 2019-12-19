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
    with open(filepath,'at') as f:
        f.write(data+'\n')

def program():
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

target = "D:/file/Picture/ACG/P站/webp/"
resultfile = "D:/Download/presult.txt"
errorfile = "D:/Download/perror.txt"
cookie = 'p_ab_id=7; p_ab_id_2=3; PHPSESSID=6001922_908f6fe4d1044fb46fc46ce4973dd168; a_type=0; b_type=1; login_ever=yes; privacy_policy_agreement=1; first_visit_datetime_pc=2018-06-21+22%3A18%3A44; p_ab_d_id=2036277048; yuid_b=FFQJZAk; module_orders_mypage=%5B%7B%22name%22%3A%22sketch_live%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22tag_follow%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22recommended_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22everyone_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22following_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22mypixiv_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22fanbox%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22featured_tags%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22contests%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22user_events%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22sensei_courses%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22spotlight%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22booth_follow_items%22%2C%22visible%22%3Atrue%7D%5D; c_type=26; tag_view_ranking=RTJMXD26Ak~0xsDLqCEW6~Lt-oEicbBr~jH0uD88V6F~BU9SQkS-zU~KN7uxuR89w~EGefOqA6KB~zIv0cf5VVk~iFcW6hPGPU~i83OPEGrYw~uusOs0ipBx~OT4SuGenFI~bXMh6mBhl8~HY55MqmzzQ~K8esoIs2eW~_pwIgrV8TB~y8GNntYHsi~jhuUT0OJva~1F9SMtTyiX~bzflrFom1W~FH69TLSzdM~qvqXJkzT2e~RybylJRnhJ~KvAGITxIxH~kP7msdIeEU~B9WjdeT8q-~9wN-K8_crj~CrFcrMFJzz~vSWEvTeZc6~qiO14cZMBI~oCR2Pbz1ly~x_jB0UM4fe~Hjx7wJwsUT~Ie2c51_4Sp~Qa8ggRsDmW~nQRrj5c6w_~ThlAk1fdQu~_RfiUqtsxe~Fq4K_8PGib~Ce-EdaHA-3~v3f3nUY-vS~YYXnZO5Qu9~MzyhgX0YIu~RqSSaz6DfD~jVbzD9UyVE~tTtqnkCOkm~vFwTRLUjL6~aUKGRzPd6e~HffPWSkEm-~TOd0tpUry5~cpt_Nk5mjc~EUwzYuPRbU~azESOjmQSV~gtqKAgwYdi~Ms9Iyj7TRt~RVRPe90CVr~w8ffkPoJ_S~sFB6DB7I46~m3EJRa33xU~_K7rbjS0MD~Fk5VbBuNbw~x8zz9iDXnd~Ow9mLSvmxK~eVxus64GZU~LJo91uBPz4~uW5495Nhg-~YRDwjaiLZn~pzzjRSV6ZO~Oa9b6mEc1T~tgP8r-gOe_~90n3-8i-qU~Mezz_Dzov-~tdV2WHpK07~VMrBpQAvH4~G-1lNBdD_I~Qdur7OglM-~0AtLJn3O6r~BLhAVeDmI2~MHugbgF9Xo~rQjRwS_xRb~m0jy1M6_jR~BQFWWhxtER~uXJn-nhV4E~kHJk-sR8-P~qtVr8SCFs5~7YXtDXab1X~gooMLQqB9a~MO67n2Zm2e~HM_o2vRZZM~6-nZ_SqrnK~KLhtt3OK7r~A3_S4dm-BR~ueeKYaEKwj~LBMc5qP5TM~65aiw_5Y72~bYfigtcm_W~UBwhLy7Ngq~mPFmmA9wY_~bdsHaxGhC9~KdHKtBPyim'

if __name__ == "__main__":
    _test_getPID()
    #print(getImgList("61791949",None))
    # list(map(print,getFileNameList(target)))
    # program()
    print("done")
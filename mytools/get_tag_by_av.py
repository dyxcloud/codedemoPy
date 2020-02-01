from urllib import request
from retrying import retry
import re
from opencc import OpenCC



httpproxy_handler = request.ProxyHandler({'http':'127.0.0.1:25378','https':'127.0.0.1:25378'})
opener = request.build_opener(httpproxy_handler)
request.install_opener(opener)

jav_host = 'www.p42u.com'
#http://www.javlibrary.com/cn/vl_searchbyid.php?keyword=ABP-933
#302跳转到真实结果
@retry(stop_max_attempt_number=3,wait_random_min=1000, wait_random_max=3000)
def get_jav(bango,byurl = False):
    url = "http://"+jav_host+"/cn/vl_searchbyid.php?keyword="+bango
    if byurl: url = bango
    req = request.Request(url)
    req.add_header('accept-language','zh-CN,zh;q=0.9')
    req.add_header('cache-control','no-cache')
    req.add_header('pragma','no-cache')
    req.add_header('referer','http://'+jav_host+'/cn/')
    req.add_header('Host',jav_host)
    req.add_header("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36")
    with request.urlopen(req,timeout=10) as f:
        if f.status == 200:
            data = f.read()
            try:
                return _parse_jav_content(data.decode('utf-8'))
            except:
                print("parse jav error bango="+bango)
    return None

re_jav_tag = re.compile(r'(rel="category tag">)(.+?)(</a></span>)')
re_jav_star = re.compile(r'(class="star"><a.+?rel="tag">)(.+?)(</a></span>)')
def _parse_jav_content(content):
    if content is None or len(content)==0 or content.isspace() :
        print("error content!")
        print(content)
        return None
    content_tag = content[content.index("类别"):content.index("演员:")]
    content_star = content[content.index("演员:"):content.index("我已经许愿了")]
    content = None
    result = []
    star_match = re.finditer(re_jav_star,content_star)
    if star_match:
        for m in star_match:
            result.append(m.group(2))
    tags_match = re.finditer(re_jav_tag,content_tag)
    if tags_match:
        for m in tags_match:
            result.append(m.group(2))

    return "#".join(result)

#https://www.javbus.com/011619_013
@retry(stop_max_attempt_number=3,wait_random_min=1000, wait_random_max=3000)
def get_javbus(bango,byurl = False):
    url = "https://www.javbus.com/"+bango
    if byurl: url = bango
    req = request.Request(url)
    req.add_header('accept-language','zh-CN,zh;q=0.9')
    req.add_header('cache-control','no-cache')
    req.add_header('pragma','no-cache')
    req.add_header('referer','https://www.javbus.com/')
    req.add_header("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36")
    with request.urlopen(req,timeout=10) as f:
        if f.status == 200:
            data = f.read()
            try:
                return _parse_javbus_content(data.decode('utf-8'))
            except:
                print("parse javbus error bango="+bango)
    return None

re_javbus_tag = re.compile(r'(name="keywords" content=")(.+)(">)')
re_javbus_star = re.compile(r'(<div class="star-name"><a href="https://www.javbus.com.+>)(.+?)(</a></div>)')
def _parse_javbus_content(content):
    if content is None or len(content)==0 or content.isspace() :
        print("error content!")
        print(content)
        return None
    content_tag = content[content.index("<meta name=\"keywords\" content=\""):content.index("<meta name=\"description\"")]
    content_star = content[content.index(">演員<"):content.index("hoverdiv")]
    content = None
    result = []
    star_match = re.finditer(re_javbus_star,content_star)
    if star_match:
        for m in star_match:
            result.append(m.group(2))
    tags_match = re.search(re_javbus_tag,content_tag)
    if tags_match:
        line = tags_match.group(2)
        line = _t2s(line[line.index(',')+1:])#去掉番号
        result.append(line)
    return "#".join(result)

cc = OpenCC('t2s')
def _t2s(str):
    return cc.convert(str)

if __name__ == "__main__":
    target = ['DAPD-003']
    for t in target:
        print(t)
        print(get_jav(t))
    print("done!")
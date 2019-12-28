from urllib import request
from retrying import retry
import re



httpproxy_handler = request.ProxyHandler({'http':'127.0.0.1:25378'})
opener = request.build_opener(httpproxy_handler)
request.install_opener(opener)

#http://www.r40z.com/cn/vl_searchbyid.php?keyword=ABP-933
#302跳转到真实结果
@retry(stop_max_attempt_number=3,wait_random_min=1000, wait_random_max=3000)
def get_jav(bango):
    url = "http://www.r40z.com/cn/vl_searchbyid.php?keyword="+bango
    req = request.Request(url)
    req.add_header('accept-language','zh-CN,zh;q=0.9')
    req.add_header('cache-control','no-cache')
    req.add_header('pragma','no-cache')
    req.add_header('referer','http://www.r40z.com/cn/')
    req.add_header("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36")
    with request.urlopen(req,timeout=10) as f:
        if f.status == 200:
            data = f.read()
            return _parse_jav_content(data.decode('utf-8'))
    return None

re_jav_tag = re.compile(r'(rel="category tag">)(.+?)(</a></span>)')
re_jav_star = re.compile(r'(class="star"><a.+rel="tag">)(.+)(</a></span>)')
def _parse_jav_content(content):
    if content is None or len(content)==0 or content.isspace() :
        print("error content!")
        print(content)
        return
    # print("start parse jav ...")
    content_tag = content[content.index("类别"):content.index("演员:")]
    content_star = content[content.index("演员:"):content.index("将这演员加入我最爱的演员名单")]
    content = None
    result = []
    star_match = re.search(re_jav_star,content_star)
    if star_match:
        result.append(star_match.group(2))
    tags_match = re.finditer(re_jav_tag,content_tag)
    if tags_match:
        for m in tags_match:
            result.append(m.group(2))

    return ",".join(result)

if __name__ == "__main__":
    target = ['MVSD-301','RCT-544','STARS-171','TKI-055','XRW-796']
    for t in target:
        print(t)
        print(get_jav(t))
    print("done!")
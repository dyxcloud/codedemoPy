import pyperclip
import requests_html


def copystr(str):
    pyperclip.copy(str)
    print('done')

class exhentaigetter:

    heads = {}
    session = requests_html.HTMLSession()

    def __init__(self,cookie):
        user_agent = requests_html.user_agent()    
        self.heads['User-Agent'] = user_agent
        self.heads['Cookie'] = cookie

    def _get_paper_url(self,url):
        r = self.session.get(url, headers=self.heads)
        es = r.html.find('.gdtm a')
        return [e.attrs['href'] for e in es]

    def _parse_paper(self,url):
        r = self.session.get(url, headers=self.heads)
        e = r.html.find('#img')
        return e[0].attrs['src']
    
    def getAllImg(self,url):
        urls = self._get_paper_url(url)
        return [self._parse_paper(u) for u in urls]

    def print_result(self,url):
        srcs = self.getAllImg(url)
        result = ''
        for src in srcs:
            print(src)
            result = result + src + '\n'
        copystr(result)

class nhentaigetter:

    heads = {}
    proxy = {'https':'127.0.0.1:25378'}
    session = requests_html.HTMLSession()

    def __init__(self,cookie):
        user_agent = requests_html.user_agent()    
        self.heads['User-Agent'] = user_agent
        self.heads['Cookie'] = cookie

    def _get_smallimg_url(self,url):
        r = self.session.get(url, headers=self.heads,proxies=self.proxy)
        es = r.html.find('.gallerythumb > img')
        return [e.attrs['data-src'] for e in es]
    
    def trans_smallimg(self,url):
        '''https://t.nhentai.net/galleries/1502218/1t.jpg
        to https://i.nhentai.net/galleries/1502218/1.jpg
        '''
        url = url.replace('https://t.nhentai.net','https://i.nhentai.net',1)
        url = url.replace('t.jpg','.jpg',1)
        url = url.replace('t.png','.png',1)
        return url

    def getAllImg(self,url):
        urls = self._get_smallimg_url(url)
        return [self.trans_smallimg(u) for u in urls]

    def print_result(self,url):
        srcs = self.getAllImg(url)
        result = ''
        for src in srcs:
            print(src)
            result = result + src + '\n'
        copystr(result)




#TODO 漫画预览页超过一页 添加翻页功能

if __name__ == "__main__":
    # cookie = 'sl=dm_1; ipb_member_id=4483572; ipb_pass_hash=b1d7d5acd649a01a1643124c8a0918a8; igneous=df9724040; sk=; yay=0; panda_width=1500'
    # getter = exhentaigetter(cookie)
    # url = 'https://exhentai.org/g/1473317/9bbf421d1a/'
    # getter.print_result(url)

    ngetter = nhentaigetter('')
    url = 'https://nhentai.net/g/280275/'
    ngetter.print_result(url)
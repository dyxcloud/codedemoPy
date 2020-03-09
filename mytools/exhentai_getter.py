import requests_html

class hentaigetter:

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
        for src in srcs:
            print(src)

#TODO 漫画预览页超过一页 添加翻页功能

if __name__ == "__main__":
    cookie = 'sl=dm_1; ipb_member_id=4483572; ipb_pass_hash=b1d7d5acd649a01a1643124c8a0918a8; igneous=df9724040; sk=; yay=0; panda_width=1500'
    getter = hentaigetter(cookie)

    url = 'https://exhentai.org/g/688441/09e456b8f5/'
    getter.print_result(url)
    print("done")

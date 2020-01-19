"""
author：Mr Yang
data: 2019/09/25
"""

import requests
from requests_toolbelt import MultipartEncoder
import re
import json
from fake_useragent import UserAgent
import os

# pip install fake-useragent  先安装此模块,生成随机user-agent
class TaoBaoSimilarityGoods():
    def __init__(self,image_path):
        self.ua = UserAgent()
        self.headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-length': '33808',
            'origin': 'https://s.taobao.com',
            'referer': 'https://s.taobao.com/search?q=&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.2&ie=utf8&initiative_id=tbindexz_20170306&tfsid=O1CN01LXS6gD1bMbNrnlZ3s_!!0-imgsearch.jpg&app=imgsearch',
            'user-agent': self.ua.random,
            'x-requested-with': 'XMLHttpRequest',
        }
        self.cookies = {'thw': 'cn', 't': 'e1cbb15ce73960500e6c937aaa9c601e', 'hng': 'CN%7Czh-CN%7CCNY%7C156', 'enc': 'x1WyS%2BusemcLY2qyObRI3t%2BAojvdQCrFYRjKT%2B5DjH1ih8WIYqImlEoVtqj%2BRAZTl632ETN%2BKKuIWUi7Rv3m4w%3D%3D', 'x': 'e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0', 'UM_distinctid': '16c8a34f6e67dc-0544b766cc5383-37c143e-144000-16c8a34f6e74b2', '_m_h5_tk': '5f9b1371af9f082b8460b8b10e9c528d_1568976050859', '_m_h5_tk_enc': 'e2313d1be40bc9fd392140817a9294dd', 'cookie2': '17360ea5d9c1b3f631bb04fc64ad716d', '_tb_token_': '5b66ebb1e3ebe', 'alitrackid': 'www.taobao.com', 'lastalitrackid': 'www.taobao.com', 'swfstore': '81337', '_uab_collina': '156937629570916079955433', 'x5sec': '7b227061696c6974616f3b32223a223861373965326261373862306637326366306661306236333962663036346431434b5751712b7746454f6962733975677272334a73674561447a49794d4441314e6a67344e6a4d794f5467374d513d3d227d', 'whl': '-1%260%260%261569376386020', 'mt': 'ci', 'cna': '6JaQFQgLnTQCAXzP+KKaCnIe', 'v': '0', 'l': 'cBOIIPyPqXu0VZzMBOCaFurza77O8IR4ouPzaNbMi_5Ik6LsPX7Ok1PqeFp6cjWdt0YB41hTyPy9-etlnzQ9CrHgcGAN.', 'isg': 'BA8PVIymjowlIopz4ojDAbWWnqPjE2NWCAgEEyEc2n6F8CzyKATzpg229iDOjjvO'}
        self.image_path = image_path


    def start_url(self):
        """获取识别后的详情链接"""
        url = 'https://s.taobao.com/image'
        data = MultipartEncoder(
            fields={
                'imgfile': (os.path.basename(self.image_path), open(self.image_path, 'rb'), 'image/jpeg')
            },
        )
        self.headers['Content-Type'] = data.content_type
        response = requests.post(url=url,data=data,headers=self.headers,cookies=self.cookies).json()
        name = response.get('name')
        if name:
            detail_url = "https://s.taobao.com/search?q=&imgfile=&js=1&stats_click=search_radio_all%253A1&initiative_id=staobaoz_20190924&ie=utf8&tfsid="+name+"&app=imgsearch"
            return detail_url


    def goods_info(self):
        """获取商品详情信息"""
        detail_url = self.start_url()
        headers = {
            'User-Agent': self.ua.random,
        }
        if detail_url:
            response = requests.get(url=detail_url, headers=headers, cookies=self.cookies)
            goods_info = json.loads(re.findall(r'g_page_config = (.*?)};', response.text)[0] + "}")['mods']['itemlist'][
                'data']['collections'][0]['auctions']
            for i in goods_info:
                print(i)
        else:
            print('无法获取到name,请尝试更换cookie')


    def cookie_method(self,cookies):
        """cookie 字符串转字典方法"""
        cookies = cookies
        cookie_dict = {}
        result = [i.split('=') for i in cookies.split('; ')]
        for item in result:
            cookie_dict[item[0]] = item[1]
        return cookie_dict






if __name__ == '__main__':
    image_path = 'C:\\000007.jpg'
    taobao = TaoBaoSimilarityGoods(image_path)
    taobao.goods_info()
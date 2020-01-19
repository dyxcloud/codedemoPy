# -*- coding=utf-8 -*-
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import json
import re


class TaobaoPicSearch():
    def __init__(self):
        self.upload_pic_url = "https://s.taobao.com/image"
        self.search_url = "https://s.taobao.com/search"
        self.proxies = {
            'socks5': 'socks5://113.100.9.40:894'
        }
        self.cookies = "thw=cn; cna=59qVFrhLAiUCAWonAeaymOv+; t=acb59ad7eaa08aad0641577a770c3c1e; cookie2=100b898ae03c7a74c32b3f0e45a5bb75; v=0; _tb_token_=71613e353b0a3; " \
                       "unb=2369529423; uc3=lg2=UtASsssmOIJ0bQ%3D%3D&vt3=F8dBxdgokw%2F7YRSNW7s%3D&id2=UUtNiSravYo28A%3D%3D&nk2=B0491LiRPA%3D%3D; csg=a563c13b; lgc=dlssnss; " \
                       "cookie17=UUtNiSravYo28A%3D%3D; dnk=dlssnss; skt=ed38c32364c2fa9b; existShop=MTU3ODAzNjQ4Nw%3D%3D; uc4=nk4=0%40BQ2MA9mNZxuAXPP%2BKSotdnsf&" \
                       "id4=0%40U2l3wtvzqa8Env2PZ0xLLhaYpd4d; tracknick=dlssnss; _cc_=V32FPkk%2Fhw%3D%3D; tg=0; _l_g_=Ug%3D%3D; sg=s3c; _nk_=dlssnss; " \
                       "cookie1=AHskQFfGi20KUZTRappiyVMcxyIe68DfNpebvIsMtUk%3D; mt=ci=95_1; uc1=cookie16=U%2BGCWk%2F74Mx5tgzv3dWpnhjPaQ%3D%3D&cookie21=VT5L2FSpccLuJBreK%2BBd&" \
                       "cookie15=WqG3DMC9VAQiUQ%3D%3D&existShop=false&pas=0&cookie14=UoTbldKQuyw0VQ%3D%3D&tag=8&lng=zh_CN; " \
                       "l=dBaL_N67QLAJI898BOfNSabqmLQOeIRb8sPPE-aUlICP_pCp59bcWZcemtT9CnGV3sLyR3SgKvQUBjYSXyUIhfF318G2cMp9hdTeR; " \
                       "isg=BDw8QnYSTsH_1XqdKkszUaJPDdounfEmtC0Pvha8SScK4d5rPkWw77IHxQmZqRi3"

    def upload_pic(self):
        headers = {
            "Host": "s.taobao.com",
            "Connection": "keep-alive",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Origin": "https://s.taobao.com",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
            "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundarySrdcfeQZ0SaGfpX8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            # "Cookie": "thw=cn; v=0; t=3a99009dee1bccd6c6e7bf0b3aaf25f2; cookie2=17126b222f2be0c12f52910d65372ccc; _tb_token_=e337e1ea1ede7; cna=PiCDFrK7vQgCAWonAeYTBj3+; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; mt=ci%3D-1_0; l=dBN2CUvIqqreZ9eWBOfiVuIJCA7O1IRf1sPzw4ON7ICPO1Cp59VOWZLpThL9CnGVnsHWR3SgKvQUBDLNmyhq6NEUE3k_J_cn3dYh.; isg=BJOTx9W4ykbjaYYSB90OYslCIhd94DZzNyiQo0WwA7LpxLBmzRtkWrTC_nQP5H8C",
            "Cookie": self.cookies,
        }
        m2 = MultipartEncoder(
            fields={
                "imgfile": ("200116105259.png", open(r"D:\Download\200116105259.png", "rb"), "image/jpeg")
            },
            boundary="----WebKitFormBoundarySrdcfeQZ0SaGfpX8"
        )
        # resp = requests.post(self.upload_pic_url, data=m2, headers=headers, timeout=10, verify=False, proxies=self.proxies)
        resp = requests.post(self.upload_pic_url, data=m2, headers=headers, timeout=10, verify=False)
        print(resp.text)
        json_resp = json.loads(resp.text)
        name = json_resp['name']
        return name

    def search(self):
        pic_name = self.upload_pic()
        params = {
            "q": "",
            "imgfile": "",
            "js": "1",
            "stats_click": "search_radio_all%3A1",
            "initiative_id": "staobaoz_20191220",
            "ie": "utf8",
            "tfsid": pic_name,  # "O1CN01sSKApU23PdGRlRdi2_!!0-imgsearch.jpg",
            "app": "imgsearch"
        }
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "referer": f"https://s.taobao.com/search?q=&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.2"
                       f"&ie=utf8&initiative_id=tbindexz_20170306&tfsid={pic_name}&app=imgsearch",  # O1CN01MpywLl1Y6cjbCRV77_!!0-imgsearch.jpg
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
            "cookie": "thw=cn; v=0; t=3a99009dee1bccd6c6e7bf0b3aaf25f2; cookie2=17126b222f2be0c12f52910d65372ccc; _tb_token_=e337e1ea1ede7; cna=PiCDFrK7vQgCAWonAeYTBj3+; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; mt=ci%3D-1_0; l=dBN2CUvIqqreZc_FBOfgNuIJCA7tWIRf1sPzw4ON7ICP_zfH59VOWZLpThYMCnGVHsLeR3SgKvQUBDLNmyhqJxpsw3k_J_mKndC..; isg=BLq603Qbs8nSOT8lxh5HvViRC-Acwy88ZhtJdMSzkc0Yt1nxrPhdVcUBBwPOJ7bd",
            # "cookie": self.cookies,
        }
        resp = requests.get(self.search_url, params=params, headers=headers, timeout=10, verify=False)
        print(resp.text)
        result = json.loads(re.search(r"g_page_config = ([\s\S]*?);", resp.text).group(1))
        title_list = []
        for i in result.get("mods", {}).get("itemlist", {}).get("data", {}).get("collections", {})[0].get("auctions"):
            print(i['raw_title'])
            title_list.append(i["raw_title"])


if __name__ == '__main__':
    pic_search = TaobaoPicSearch()
    # pic_search.search()
    result = pic_search.upload_pic()
    print("===="+result)

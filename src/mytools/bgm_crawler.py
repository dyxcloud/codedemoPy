import requests_html
import sqlite3
import os
import re
from datetime import datetime


class DbOperator:
    db_path = os.path.abspath('../../data/test.db')
    conn = sqlite3.connect(os.path.abspath(db_path), isolation_level=None)
    cursor = conn.cursor()

    def __init__(self):
        super().__init__()

    def check(self, subject_id):
        """判断是否存在, 如果存在再判断是否检查过"""
        sql = "select subject_id from bgm_subject where subject_id=?"
        self.cursor.execute(sql, (subject_id,))
        if self.cursor.rowcount > 0:
            print("___找到旧数据, 执行删除")
            self.delete(subject_id)

    def delete(self, subject_id):
        sql = "delete from bgm_subject where subject_id=?"
        self.cursor.execute(sql, (subject_id,))
        return self.cursor.rowcount

    def insert(self, param_dic):
        s_id = int(param_dic['subject_id'])
        self.check(s_id)
        sql = "insert into bgm_subject values (?,?,?,?,?,?,?,?,?,?,?,?,?)"
        date = str(datetime.now().replace(microsecond=0))
        values = [param_dic['subject_id'], param_dic['name'], param_dic['name_cn'], param_dic['point'],
                  param_dic['rank'], param_dic['votes'],
                  param_dic['date'], param_dic['wanted'], param_dic['watched'], param_dic['watching'],
                  param_dic['hold'], param_dic['drop'], date]
        self.cursor.execute(sql, values)

    def close(self):
        self.cursor.close()
        self.conn.close()


# noinspection PyUnresolvedReferences
class BgmCrawler:
    user_agent = requests_html.user_agent(style='chrome')
    cookie = {"chii_sid": "LkWJmq"}
    heads = {'User-Agent': user_agent}
    proxies = {}
    session = requests_html.HTMLSession()

    def __init__(self):
        super().__init__()

    def get_subject_list(self, target_url):
        """获取待抓取url"""
        r = self.session.get(target_url, headers=self.heads, proxies=self.proxies)
        html = r.html
        a_list = html.find("#browserItemList > li > a")
        url_list = []
        for a in a_list:
            url_list.append(a.absolute_links.pop())
        # 下一页
        last_page = html.find(".page_inner>:last-child")[0]
        if last_page.tag is 'a':
            print("下一页...")
            sub_result = self.get_subject_list(target_url.split("?")[0] + last_page.links.pop())
            url_list += sub_result
        return url_list

    def get_detail(self, target_url, need_cookie=False):
        """获取详情信息"""
        if need_cookie:
            r = self.session.get(target_url, headers=self.heads, cookies=self.cookie, proxies=self.proxies)
        else:
            r = self.session.get(target_url, headers=self.heads, proxies=self.proxies)
        html = r.html
        # noinspection PyDictCreation
        result = {
            "subject_id": None, "name": None, "name_cn": None,
            "point": None, "rank": None, "votes": None, "date": None,
            "wanted": None, "watched": None, "watching": None, "hold": None, "drop": None
        }
        result["subject_id"] = target_url.split("/")[-1]
        # 判断是否需要登录抓取
        if not need_cookie and len(html.find("h1.nameSingle>a")) == 0 and len(html.find("#colunmNotice")) > 0:
            return self.get_detail(target_url, True)
        title = html.find("h1.nameSingle>a")[0]
        result["name"] = title.text
        result["name_cn"] = title.attrs["title"]
        result["point"] = html.find("div.global_score>span")[0].text
        rank = html.find("div.global_score>div>small:last-child")[0].text[1:]
        if rank != '-':
            result["rank"] = rank
        result["votes"] = html.find("span[property='v:votes']")[0].text
        match = re.search(r'\d{4}年\d+月\d+日', html.find("ul#infobox")[0].text)
        if match:
            result["date"] = match.group(0)
        # 解析人数
        line = html.find("div#subjectPanelCollect>span.tip_i")[0].text
        match = re.search(r'(?<= )\d+(?=人想看)', line)
        if match:
            result["wanted"] = match.group(0)
        match = re.search(r'(?<= )\d+(?=人看过)', line)
        if match:
            result["watched"] = match.group(0)
        match = re.search(r'(?<= )\d+(?=人在看)', line)
        if match:
            result["watching"] = match.group(0)
        match = re.search(r'(?<= )\d+(?=人搁置)', line)
        if match:
            result["hold"] = match.group(0)
        match = re.search(r'(?<= )\d+(?=人抛弃)', line)
        if match:
            result["drop"] = match.group(0)
        return result


def crawler_tag_list(list_page):
    c = BgmCrawler()
    db_operator = DbOperator()
    url_list = c.get_subject_list(list_page)
    print("获取到{}个url".format(len(url_list)))
    for url in url_list:
        print("开始解析:{}".format(url))
        result = c.get_detail(url)
        print("解析完成,{}".format(result))
        db_operator.insert(result)
    db_operator.close()


if __name__ == '__main__':
    # crawler_tag_list("https://bgm.tv/anime/tag/2021%E5%B9%B44%E6%9C%88")
    crawler = BgmCrawler()
    result = crawler.get_detail("https://bgm.tv/subject/175600", False)
    print(result)
    # db_operator = DbOperator()
    # db_operator.insert(result)
    # db_operator.close()

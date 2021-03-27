import requests_html
import sqlite3
import os

dic = {'subject_id': '301469', 'name': '100万の命の上に俺は立っている', 'name_cn': '我立于百万生命之上', 'point': '5.8', 'rank': '5622',
       'votes': '797', 'date': '2020年10月2日', 'wanted': '164', 'watched': '887', 'watching': '228', 'hold': '89',
       'drop': '221'}


class DbOperator:
    db_path = os.path.abspath('../../data/test.db')
    conn = sqlite3.connect(os.path.abspath(db_path), isolation_level=None)
    cursor = conn.cursor()

    def __init__(self):
        super().__init__()

    def count(self, subject_id):
        sql = "select count(*) from bgm_subject where subject_id=?"
        self.cursor.execute(sql, (subject_id,))
        return self.cursor.fetchone()[0]

    def delete(self, subject_id):
        sql = "delete from bgm_subject where subject_id=?"
        self.cursor.execute(sql, (subject_id,))
        return self.cursor.rowcount

    def insert(self, param_dic):
        s_id = int(param_dic['subject_id'])
        if self.count(s_id) > 0:
            self.delete(s_id)
        sql = "insert into bgm_subject values (?,?,?,?,?,?,?,?,?,?,?,?)"
        values = [param_dic['subject_id'], param_dic['name'], param_dic['name_cn'], param_dic['point'], param_dic['rank'], param_dic['votes'],
                  param_dic['date'], param_dic['wanted'], param_dic['watched'], param_dic['watching'], param_dic['hold'], param_dic['drop']]
        self.cursor.execute(sql, values)

    def close(self):
        self.cursor.close()
        self.conn.close()


class BgmCrawler:
    user_agent = requests_html.user_agent(style='chrome')
    heads = {'User-Agent': user_agent}
    proxies = {}
    session = requests_html.HTMLSession()

    def __init__(self):
        super().__init__()

    def _get_subject_list(self, target_url):
        """获取待抓取url"""
        r = self.session.get(target_url, headers=self.heads, proxies=self.proxies)
        html = r.html
        a_list = html.find("#browserItemList > li > a")
        result = []
        for a in a_list:
            result.append(a.absolute_links.pop())
        # 下一页
        last_page = html.find(".page_inner>:last-child")[0]
        if last_page.tag is 'a':
            print("下一页...")
            sub_result = self._get_subject_list(target_url.split("?")[0] + last_page.links.pop())
            result += sub_result
        return result

    def _get_detail(self, target_url):
        """获取详情信息"""
        r = self.session.get(target_url, headers=self.heads, proxies=self.proxies)
        html = r.html
        result = {}
        result["subject_id"] = target_url.split("/")[-1]
        title = html.find("h1.nameSingle>a")[0]
        result["name"] = title.text
        result["name_cn"] = title.attrs["title"]
        result["point"] = html.find("div.global_score>span")[0].text
        result["rank"] = html.find("div.global_score>div>small:last-child")[0].text[1:]
        result["votes"] = html.find("span[property='v:votes']")[0].text
        result["date"] = html.find("ul#infobox>li")[2].text[6:]
        result["wanted"] = html.find("div#subjectPanelCollect>span.tip_i>a")[0].text[0:-3]
        result["watched"] = html.find("div#subjectPanelCollect>span.tip_i>a")[1].text[0:-3]
        result["watching"] = html.find("div#subjectPanelCollect>span.tip_i>a")[2].text[0:-3]
        result["hold"] = html.find("div#subjectPanelCollect>span.tip_i>a")[3].text[0:-3]
        result["drop"] = html.find("div#subjectPanelCollect>span.tip_i>a")[4].text[0:-3]
        return result


def func():
    crawler = BgmCrawler()
    result = crawler._get_detail("https://bgm.tv/subject/301469")
    print(result)


if __name__ == '__main__':
    db = DbOperator()
    db.insert(dic)
    db.close()

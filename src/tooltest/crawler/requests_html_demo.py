import requests_html

heads = {}
user_agent = requests_html.user_agent(style='chrome')    
heads['User-Agent'] = user_agent
print(user_agent)


session = requests_html.HTMLSession()
r = session.get('http://item.taobao.com/item.htm?id=613451971817', headers=heads)
print(r.text)
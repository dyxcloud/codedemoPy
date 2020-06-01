from selenium import webdriver
import time

class pidp():
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.set_window_size(1700,1000)

    def login(self,username, password):
        self.driver.get('http://www.iprdp.cn/login.html')
        time.sleep(1)
        self.driver.find_element_by_css_selector('body > div.main > div > div > div.login-panel.fr.bgf > div.login-way-content.now > div.login-panel-item.account-panel > div:nth-child(1) > label > input[type=text]').click()
        self.driver.find_element_by_css_selector('body > div.main > div > div > div.login-panel.fr.bgf > div.login-way-content.now > div.login-panel-item.account-panel > div:nth-child(1) > label > input[type=text]').clear()
        self.driver.find_element_by_css_selector('body > div.main > div > div > div.login-panel.fr.bgf > div.login-way-content.now > div.login-panel-item.account-panel > div:nth-child(1) > label > input[type=text]').send_keys(username)
        time.sleep(1)
        self.driver.find_element_by_css_selector('body > div.main > div > div > div.login-panel.fr.bgf > div.login-way-content.now > div.login-panel-item.account-panel > div:nth-child(2) > label > input[type=password]').click()
        self.driver.find_element_by_css_selector('body > div.main > div > div > div.login-panel.fr.bgf > div.login-way-content.now > div.login-panel-item.account-panel > div:nth-child(2) > label > input[type=password]').clear()
        self.driver.find_element_by_css_selector('body > div.main > div > div > div.login-panel.fr.bgf > div.login-way-content.now > div.login-panel-item.account-panel > div:nth-child(2) > label > input[type=password]').send_keys(password)
        time.sleep(1)
        self.driver.find_element_by_id('submit-btn').click()
        time.sleep(3)

    def startTask(self):
        self.driver.find_element_by_css_selector('body > div > div.layui-side.kit-side.pub-l-side > div > ul > li:nth-child(2) > a > span:nth-child(2)').click()
        time.sleep(1)
        self.driver.find_element_by_css_selector('body > div.layui-layout.layui-layout-admin.kit-layout-admin > div.layui-side.kit-side.pub-l-side > div > ul > li.layui-nav-item.layui-nav-itemed > dl > dd:nth-child(1) > a > span').click()
        time.sleep(5)
        xf = self.driver.find_element_by_xpath('//*[@id="container"]/div/div/div[2]/iframe')
        self.driver.switch_to.frame(xf)
        self.driver.find_element_by_css_selector('#content1 > div > table > tbody > tr:nth-child(1) > td.operating.flexDiv > div > span.task_switch > i').click()
        time.sleep(1)
        self.driver.find_element_by_css_selector('#configProduct > ul > li:nth-child(1) > div > div > div:nth-child(1) > img').click()
        self.driver.find_element_by_css_selector('#configProduct > ul > li:nth-child(1) > div > div > div:nth-child(2) > img').click()
        self.driver.find_element_by_css_selector('#configProduct > ul > li:nth-child(2) > div > div > div > span').click()

        self.driver.find_element_by_css_selector('#configProduct > div.product_btn > span.product_sure.layui-btn').click()
        time.sleep(1)
        self.driver.find_element_by_xpath('/html/body/div[14]/div[3]/a[1]').click()
        time.sleep(1)
        self.driver.find_element_by_xpath('/html/body/div[6]/div[2]/div/div[3]/span[1]').click()
        time.sleep(3)

    def logout(self):
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div[3]/a').click()
        time.sleep(1)
    
    def quit(self):
        self.driver.close()
        self.driver.quit()

def program():
    p = pidp()
    users = ['apptest'+str(x) for x in range(894,1000)]
    for user in users:
        print(user)
        p.login(user,'cnpat6')
        p.startTask()
        p.logout()
    p.quit()


if __name__ == "__main__":
    program()

from selenium import webdriver
import time


class Sounimei(object):
    def __init__(self):
        # 配置Chrome
        options = webdriver.ChromeOptions()
        # profile.default_content_settings.popups：设置为 0 禁止弹出窗口
        # download.default_directory: 设置下载路径
        self.PATH = '/Users/teihate/Downloads'  # 需要使用绝对路径
        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': self.PATH}
        options.add_experimental_option('prefs', prefs)

        self.driver = webdriver.Chrome(chrome_options=options)

        # 定义睡眠时间
        self.SLEEP_TIME = 1

        # 隐性等待时间
        self.WAIT_TIME = 1

    def login(self):
        url = 'https://wsmusic.sounm.com/'
        self.driver.get(url)
        time.sleep(self.SLEEP_TIME)
        self.driver.implicitly_wait(self.WAIT_TIME)
        img_url = self.driver.find_element_by_tag_name('img').get_attribute('src')
        input = self.driver.find_element_by_css_selector('input.van-field__control')
        button = self.driver.find_element_by_tag_name('button')
        self.get_Code(img_url)
        time.sleep(self.SLEEP_TIME)
        # 可以利用二维码工具自动登陆
        input.send_keys('8943')
        time.sleep(self.SLEEP_TIME)
        button.click()
        time.sleep(self.SLEEP_TIME)
        self.download()

    def download(self):
        search_btn = self.driver.find_element_by_tag_name('button')
        # key = input('请输入搜索关键字\n')
        key_input = self.driver.find_element_by_class_name('van-field__control')
        key_input.send_keys('五月天')

        search_btn.click()

        list = self.driver.find_elements_by_css_selector('.song-item-cell span.item-title')
        for index, song in enumerate(list):
            self.driver.implicitly_wait(self.WAIT_TIME)
            song.click()
            self.driver.implicitly_wait(self.WAIT_TIME)
            flac_btn = self.driver.find_element_by_css_selector('div.song-item-cell-padding:nth-of-type(2) span')
            flac_btn.click()
            name = self.driver.find_element_by_css_selector('van-cell__value van-cell__value--alone').text
            url = self.driver.find_element_by_css_selector('div.song-item-cell-padding:nth-of-type(2) div.van-cell__value').get_attribute('href')
            print(name + ':' + url)

    def run(self):
        self.login()


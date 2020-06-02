from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

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

    # 进行解锁
    def unlock(self):
        url = 'https://wsmusic.sounm.com/unlock'
        self.driver.get(url)
        time.sleep(self.SLEEP_TIME)
        self.driver.implicitly_wait(self.WAIT_TIME)
        img_url = self.driver.find_element_by_tag_name('img').get_attribute('src')
        input = self.driver.find_element_by_css_selector('input.van-field__control')
        s_button = self.driver.find_element_by_tag_name('button')
        time.sleep(self.SLEEP_TIME)
        # 可以利用二维码工具自动登陆
        key =  self.get_Code(img_url)
        input.send_keys(key)
        time.sleep(self.SLEEP_TIME)
        s_button.click()
        time.sleep(self.SLEEP_TIME)

    # 解析二维码
    def get_Code(self, url):
        # key = input('请输入扫码后结果:\n')
        key = '8943'
        return key

    # 音乐下载
    def download(self):
        result = []
        time.sleep(5)
        search_btn = self.driver.find_element_by_tag_name('button')
        # key = input('请输入搜索关键字\n')
        key_input = self.driver.find_element_by_class_name('van-field__control')
        key_input.clear()
        key_input.send_keys('Justin Bieber')
        search_btn.click()
        time.sleep(5)
        self.show_more()

        list = self.driver.find_elements_by_css_selector('.song-item-cell span.item-title')
        for index, song in enumerate(list):
            try:
                song.click()
                time.sleep(3)
                try:
                    flac_btn = self.driver.find_element_by_css_selector(
                        'div.song-item-cell-padding:nth-of-type(2) span')
                    flac_btn.click()
                    time.sleep(3)
                    try:
                        url = self.driver.find_element_by_tag_name('a').get_attribute('href')
                        result.append(url)
                        print(url)
                        close_btn = self.driver.find_element_by_css_selector('div:nth-of-type(4) i')
                        close_btn.click()
                        time.sleep(2)
                    except:
                        print('获取信息失败')
                        close_btn = self.driver.find_element_by_css_selector('div:nth-of-type(4) i')
                        close_btn.click()
                        time.sleep(2)
                except:
                    print('FLAC点击失败')
                    close_btn = self.driver.find_element_by_css_selector('i.van-icon-cross')
                    close_btn.click()
                    time.sleep(2)
            except:
                print('歌曲点击失败')

        print(result)

    def run(self):
        self.unlock()
        self.download()


    def show_more(self):
        try:
            print('请在60s内刷新页面')
            time.sleep(60)
        except:
            print('加载失败')
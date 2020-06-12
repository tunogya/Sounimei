import string

import requests
import zxing
from selenium import webdriver
import time
import csv
import os

class Sounimei(object):
    def __init__(self):
        # 配置Chrome
        options = webdriver.ChromeOptions()
        self.PATH = '/Users/teihate/Downloads'  # 需要使用绝对路径
        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': self.PATH}
        options.add_experimental_option('prefs', prefs)
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--ignore-certificate-errors')
        self.driver = webdriver.Chrome(chrome_options=options)
        # 定义睡眠时间
        self.SLEEP_TIME = 1
        # 隐性等待时间
        self.WAIT_TIME = 1
        # 下载的最大数量
        self.MAX_SONG_QUANTITY = 50
        # 设置CSV文件
        self.CSV_FILE_NAME = 'Results.csv'
        # 存储CSV数据
        self.csv_data = []

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
        key = self.get_Code(img_url)
        # key = "8943"
        input.send_keys(key)
        time.sleep(self.SLEEP_TIME)
        s_button.click()
        time.sleep(self.SLEEP_TIME)

    # 解析二维码
    def get_Code(self, url):
        # 定义下载函数
        response = requests.get(url)
        # 获取的文本实际上是图片的二进制文本
        img = response.content
        try:
            # 将他拷贝到本地文件 w 写  b 二进制  wb代表写入二进制文本
            with open(self.PATH + '/a.jpg', 'wb') as f:
                f.write(img)
            reader = zxing.BarCodeReader()
            barcode = reader.decode(self.PATH + '/a.jpg')
            code = barcode.parsed
            print('破解验证成功')
            return code[-4:]
        except Exception as e:
            # 若没有java环境，使用手动模式
            print(e)
            code = input('请输入扫描后验证码\n')
            return code

    # 下载文件
    def download(self, url):
        file_name = url[32:55]   #获取文件名
        if not os.path.exists(self.PATH + '/' + file_name):
            r = requests.get(url)
            with open(self.PATH + '/' + file_name, "wb") as f:
                f.write(r.content)
            f.close()
        else:
            print(file_name + '已存在')

    # 音乐检索
    def search(self):
        time.sleep(5)
        search_btn = self.driver.find_element_by_tag_name('button')
        key = input('请输入搜索关键字\n')
        key_input = self.driver.find_element_by_class_name('van-field__control')
        key_input.clear()
        key_input.send_keys(key)
        search_btn.click()
        time.sleep(5)
        count = input('请输入下滑次数\n')
        self.show_more(int(count))

        list = self.driver.find_elements_by_css_selector('.song-item-cell')
        for index, song in enumerate(list):
            try:
                title = song.find_element_by_css_selector('span.item-title').text
                album = song.find_element_by_css_selector('span.item-album').text
                singer = song.find_element_by_css_selector('.van-cell__label span:nth-of-type(1)').text
                song.click()
                time.sleep(3)
                try:
                    flac_btn = self.driver.find_element_by_css_selector(
                        'div.song-item-cell-padding:nth-of-type(2) span')
                    flac_btn.click()
                    time.sleep(3)
                    try:
                        url = self.driver.find_element_by_tag_name('a').get_attribute('href')
                        self.download(url)
                        row = [title, album, singer, url]
                        print(row)
                        close_btn = self.driver.find_element_by_css_selector('div:nth-of-type(4) i')
                        close_btn.click()
                        time.sleep(2)
                        self.csv_data.append(row)
                        self.write_to_csv()
                    except Exception as e:
                        print(e)
                        close_btn = self.driver.find_element_by_css_selector('div:nth-of-type(4) i')
                        close_btn.click()
                        time.sleep(2)
                except Exception as e:
                    print(e)
                    close_btn = self.driver.find_element_by_css_selector('i.van-icon-cross')
                    close_btn.click()
                    time.sleep(2)
            except Exception as e:
                print(e)

    # 手动加载歌曲
    def show_more(self, count):
        # 滑动到最底部
        print('下拉页面中')
        for i in range(1, count):
            self.driver.execute_script('window.scrollBy(0, 1000)')
            time.sleep(2)
        # 滑动到最顶部
        print('开始下载')
        self.driver.execute_script('window.scrollTo(0,0)')
        time.sleep(3)

    # 写入到csv
    def write_to_csv(self):
        with open(self.PATH + '/' + self.CSV_FILE_NAME, 'w') as csvfile:
            spam_writer = csv.writer(csvfile, dialect='excel')
            str.encode("utf-8")
            spam_title = ['歌曲名', '专辑', '歌手', '下载地址']
            spam_writer.writerow(spam_title)
            for item in self.csv_data:
                spam_writer.writerow(item)

    # 运行函数
    def run(self):
        self.unlock()
        self.search()
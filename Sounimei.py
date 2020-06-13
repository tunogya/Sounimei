import requests
import zxing
from selenium import webdriver
import time
import os
import re
import connectDB


class Sounimei(object):
    def __init__(self):
        # 配置Chrome
        options = webdriver.ChromeOptions()
        # 设置图片不加载
        options.add_argument('blink-settings=imagesEnabled=false')
        # 设置无头浏览器模式
        options.add_argument('--headless')
        options.add_argument('–-disable-gpu')
        options.add_argument('–-no-sandbox')
        options.add_argument('–-disable-dev-shm-usage')
        options.add_argument('–-disable-extensions')
        # profile.default_content_settings.popups：设置为 0 禁止弹出窗口
        # download.default_directory: 设置下载路径
        self.PATH = '/Users/teihate/Downloads'  # 需要使用绝对路径
        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': self.PATH}
        options.add_experimental_option('prefs', prefs)

        # self.driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=options)
        self.driver = webdriver.Chrome(chrome_options=options)
        # 定义睡眠时间
        self.SLEEP_TIME = 1
        # 隐性等待时间
        self.WAIT_TIME = 1

        # table_name = input("请输入表格名称")
        table_name = 'qq_music'
        # 预创建表存储结果
        connectDB.my_create_table(table_name)

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
    def download(self, url, file_name):
        if not os.path.exists(self.PATH + '/' + file_name):
            r = requests.get(url)
            with open(self.PATH + '/' + file_name, "wb") as f:
                f.write(r.content)
            f.close()
        else:
            print(file_name + '已存在')

    # 音乐检索key关键词
    def search(self, key, count):
        time.sleep(5)
        search_btn = self.driver.find_element_by_tag_name('button')
        key_input = self.driver.find_element_by_class_name('van-field__control')
        key_input.clear()
        key_input.send_keys(key)
        search_btn.click()
        time.sleep(5)
        self.show_more(int(count))

        list = self.driver.find_elements_by_css_selector('.song-item-cell')
        for index, song in enumerate(list):
            try:
                result = {}
                result['title'] = song.find_element_by_css_selector('span.item-title').text
                result['album'] = song.find_element_by_css_selector('span.item-album').text
                result['singer'] = song.find_element_by_css_selector('.van-cell__label span:nth-of-type(1)').text
                song.click()
                time.sleep(3)
                try:
                    flac_btn = self.driver.find_element_by_css_selector(
                        'div.song-item-cell-padding:nth-of-type(2) span')
                    flac_btn.click()
                    time.sleep(3)
                    try:
                        result['url'] = self.driver.find_element_by_tag_name('a').get_attribute('href')
                        pattern = re.compile(r"(F.+(?=\?guid))")
                        result['file_name'] = re.findall(pattern, result['url'])[0]
                        connectDB.my_insert_result(result)
                        # self.download(result['url'], result['file_id'])   # 下载
                        # print(result)
                        close_btn = self.driver.find_element_by_css_selector('div:nth-of-type(4) i')
                        close_btn.click()
                        time.sleep(2)
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

    # 通过下滑加载歌曲
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

    # 运行函数
    def run(self):
        self.unlock()
        key = input('Input your fantastic:')
        count = input('How many times to scroll the window:')
        self.search(key, count)

    # 遍历查询所有的歌手
    def collection(self):
        begin = int(input('Begin number:')) - 1
        end = int(input('End number:'))
        list = connectDB.my_query_singer(begin, end)
        print(list)
        self.unlock()
        for singer in enumerate(list):
            self.search(singer, 100)



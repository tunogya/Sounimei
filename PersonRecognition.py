from selenium import webdriver
import time
import zxing
import os
import requests
import traceback

driver = webdriver.Chrome()


# 加载二维码
def loadQcode():
    driver.get("https://wsmusic.sounm.com/unlock")
    img_url = driver.find_element_by_css_selector("img")
    url = img_url.get_attribute("src")
    # img_name = url.split('/')[-1:]

    print(url)
    return url

# 定义下载函数
def downLoad(url):
    response = requests.get(url)
    # 获取的文本实际上是图片的二进制文本
    img = response.content
    # 将他拷贝到本地文件 w 写  b 二进制  wb代表写入二进制文本
    with open('./a.jpg', 'wb') as f:
        f.write(img)



def scanQcode():
    # 识别二维码
    reader = zxing.BarCodeReader()
    # barcode = reader.decode("https://cdn.dnpw.org/api/qrcode/cache/fecb8b7504959d5a7f4aff400f2db9c3.png_300_300_2_95.jpg")
    # print(barcode.parsed)


if __name__ == '__main__':
    url = loadQcode()
    downLoad(url)
    time.sleep(2)
    driver.quit()

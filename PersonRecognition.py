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
    unlockUrl = img_url.get_attribute("src")
    # img_name = url.split('/')[-1:]

    print(unlockUrl)
    return unlockUrl


# 定义下载函数
def downLoad(url):
    response = requests.get(url)
    # 获取的文本实际上是图片的二进制文本
    img = response.content
    # 将他拷贝到本地文件 w 写  b 二进制  wb代表写入二进制文本
    with open('./img/a.jpg', 'wb') as f:
        f.write(img)


# 识别二维码
def scanQcode():
    reader = zxing.BarCodeReader()
    barcode = reader.decode("./img/a.jpg")
    code = barcode.parsed

    return code[-4:]


# 填写解析过的二维码，并且输入点击跳转到index
def inputQcode(codeVan):
    vanInput = driver.find_element_by_css_selector("input.van-field__control")
    vanInput.send_keys(codeVan)
    # 点击发送
    driver.find_element_by_css_selector("button").click()


if __name__ == '__main__':
    url = loadQcode()
    downLoad(url)
    code = scanQcode()
    inputQcode(code)
    time.sleep(2)
    #driver.quit()

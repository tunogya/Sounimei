import threading
from urllib.request import *


# Download类：包含download()和get_complete_rate()两种方法。
class Download():
    def __int__(self, link, file_path, thread_num):
        self.link = link
        self.file_path = file_path
        self.thread_num = thread_num
        self.threads = []

    # download()方法种首先用 urlopen() 方法打开远程资源并通过 Content-Length获取资源的大小，
    # 然后计算每个线程应该下载网络资源的大小及对应部分吗，最后依次创建并启动多个线程来下载网络资源的指定部分。
    def download(self):
        req = Request(url=self.link, method='GET')
        req.add_header('Accept', '*/*')
        req.add_header('Charset', 'UTF-8')
        req.add_header('Connection', 'Keep-Alive')
        f = urlopen(req)

        # 获取下载文件的大小
        self.file_size = int(dict(f.headers).get('Content-Length', 0))
        f.close()
        # 计算每个需要下载的资源的大小
        current_part_size = self.file_size // self.thread_num + 1
        for i in range(self.thread_num):
            # 计算每个线程的下载位置
            start_pos = i * current_part_size
            t = open(self.file_path, 'wb')
            t.seek(start_pos, 0)
            # 创建下载线程
            td = ThreadDownload(self.link, start_pos, current_part_size, t)
            self.threads.append(td)
            td.start()

    # get_complete_rate()则是用来返回已下载的部分占全部资源大小的比例，用来回显进度。
    def get_complete_rate(self):
        sum_size = 0
        for i in range(self.thread_num):
            sum_size += self.threads[i].length
        return sum_size / self.file_size


# ThreadDownload类：该线程类继承了threading.Thread类，包含了一个run()方法。
class ThreadDownload(threading.Thread):
    def __init__(self, link, start_pos, current_part_size, current_part):
        super().__init__()
        # 下载路径
        self.link = link
        # 当前线程的下载位置
        self.start_pos = start_pos
        # 当前线程负责下载的文件大小
        self.current_part_size = current_part_size
        # 当前文件需要下载的文件块
        self.current_part = current_part
        # 定义该线程已经下载的字节数
        self.length = 0

    # run()方法主要负责每个线程读取网络数据并写入本地。
    def run(self):
        req = Request(url = self.link, method='GET')
        req.add_header('Accept', '*/*')
        req.add_header('Charset', 'UTF-8')
        req.add_header('Connection', 'Keep-Alive')

        f = urlopen(req)
        # 跳过self.start_pos个字节，只下载自己负责的那部分内容
        for i in range(self.start_pos):
            f.read(1)
        while self.length < self.current_part_size:
            data = f.read(1024)
            if data is None or len(data) <= 0:
                break
            self.current_part.write(data)
            self.length += len(data)
        self.current_part.close()
        f.close()
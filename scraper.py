from Sounimei import Sounimei


if __name__ == '__main__':
    path = input("File download path:")
    table_name = 'qq_music'
    key = input('Input your fantastic:')
    spider = Sounimei(path=path, table_name=table_name, key=key)
    spider.run()
    # spider.collection()
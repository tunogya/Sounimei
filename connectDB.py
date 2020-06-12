import pymysql

# 打开数据库连接（ip/用户名/密码/数据库名）
host = input("请输入数据库地址\n")
user = input("请输入数据库用户名\n")
password = input("请输入数据库密码\n")
table = "music"
db = pymysql.connect(host, user, password, table)

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用 execute() 方法执行 SQL 查询
cursor.execute("SET NAMES utf8")
cursor.execute("SET CHARACTER_SET_CLIENT = utf8")
cursor.execute("SET CHARACTER_SET_RESULTS = utf8")


def my_insert_result(result):
    try:
        title = result['title']
        singer = result['singer']
        album = result['album']
        file_name = result['file_name']
        url = result['url']
        sql = "INSERT INTO `qq_music` (`title`, `singer`, `album`, `file_name`, `url`) VALUE ('" + \
              title + "','" + singer + "','" + album + "','" + file_name + "','" + url + "');"
        cursor.execute(sql)
        db.commit()
        print("《" + title + "》写入数据库")
    except Exception as e:
        # 如果发生错误则回滚
        print("《" + title + "》写入数据库失败")
        print(e)
        db.rollback()
        # db.close()
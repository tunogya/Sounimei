import pymysql

# 打开数据库连接（ip/用户名/密码/数据库名）
user = input("请输入数据库用户名\n")
password = input("请输入数据库密码\n")
db = pymysql.connect("122.152.201.37", user, password, "music")

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用 execute() 方法执行 SQL 查询
cursor.execute("SET NAMES utf8")
cursor.execute("SET CHARACTER_SET_CLIENT = utf8")
cursor.execute("SET CHARACTER_SET_RESULTS = utf8")


def my_query_exist(file_id):
    try:
        sql = '''
            SELECT *
            FROM `qq_music`
            WHERE `file_id` = "''' + file_id + '''" 
        '''
        cursor.execute(sql)
        results = cursor.fetchall()

        if len(results) == 0:
            return 0
        else:
            return 1
    except Exception as e:
        print(e)


def my_insert_result(result):
    try:
        title = result['title']
        singer = result['singer']
        album = result['album']
        file_id = result['file_id']
        url = result['url']
        sql = "INSERT INTO `qq_music` (`title`, `singer`, `album`, `file_id`, `url`) VALUE ('" + \
              title + "','" + singer + "','" + album + "','" + file_id + "','" + url + "');"
        cursor.execute(sql)
        db.commit()
        print("《" + title + "》写入数据库")
    except Exception as e:
        # 如果发生错误则回滚
        print("《" + title + "》写入数据库失败")
        print(e)
        db.rollback()
        # db.close()
import pymysql

# 打开数据库连接（ip/用户名/密码/数据库名）
host = input("Database host:")
user = input("Database username:")
password = input("Database password:")
schema = "music"
db = pymysql.connect(host, user, password, schema)

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用 execute() 方法执行 SQL 查询
cursor.execute("SET NAMES utf8")
cursor.execute("SET CHARACTER_SET_CLIENT = utf8")
cursor.execute("SET CHARACTER_SET_RESULTS = utf8")


def my_create_table(table_name):
    try:
        sql = '''
        CREATE TABLE `''' + table_name + '''`  (
      `id` int(11) NOT NULL,
      `file_name` varchar(24) NOT NULL,
      `title` varchar(255) NOT NULL,
      `singer` varchar(255) NOT NULL,
      `album` varchar(255) NOT NULL,
      `url` varchar(255) NOT NULL,
      PRIMARY KEY (`id`),
      INDEX `index`(`title`, `singer`, `album`) USING HASH,
      UNIQUE INDEX `unique`(`file_name`) USING HASH
    )
        '''
        cursor.execute(sql)
        print('初始化表成功')
    except Exception as e:
        print(e)


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
        print("《" + title + "》Write Successful!")
    except Exception as e:
        # 如果发生错误则回滚
        print("《" + title + "》Write Fail!")
        print(e)
        db.rollback()
        # db.close()


def my_query_singer(begin, end):
    try:
        sql = "SELECT `name`  FROM `singer` ORDER BY `id` LIMIT " + str(begin) + ", " + str(end)
        cursor.execute(sql)
        result = cursor.fetchall()
        singers = []
        for singer in result:
            singers.append(singer[0])
        return singers
    except Exception as e:
        print(e)
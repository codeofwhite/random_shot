# 插入数据库
import pymysql
import mysql.connector


# 连接数据库

def connectdb():
    print("连接SQL服务器")
    db = mysql.connector.connect(host="localhost", port=3307, user="root", password="Jason20040903")
    print("连接上了！")
    return db


# 插入数据
def insertdb(db, db_data):
    """ 插入数据 """
    global i
    cursor = db.cursor()  # 游标
    use = "use score"
    sql = "insert into scores(score_num)VALUES(%d)" % (db_data[0])
    # cursor = conn.cursor()
    # sql = "insert into user_base_info(user_name,user_password)VALUES(%s,%s)"
    # cursor.execute('use user_info')
    # cursor.execute(sql, (entry_name, entry_pass))
    # conn.commit()
    cursor.execute(use)
    cursor.execute(sql)  # 执行sql语句
    db.commit()  # 执行成功，提交
    print('成功提交')
    # except Exception:
    #     db.rollback()  # 发生错误，回滚
    #     print('错误')


score = 1000

db_data = []
db_data.append(score)
db = connectdb()
insertdb(db, db_data)

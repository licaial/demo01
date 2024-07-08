# 所有和数据库有关的函数方法
import pymysql
# 定义和数据库的连接
conn = pymysql.connect(
    host="rm-2zeow21tg8mb0iwb7wo.mysql.rds.aliyuncs.com",
    port=3306,
    user="root",
    passwd="Root123456",
    db="assistant",
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor
)

# 1、根据用户名查询用户的函数
def query_user_by_username(username):
    sql = "select * from sys_user where username = %s"
    cur = conn.cursor()
    cur.execute(sql, [username])
    result = cur.fetchone()
    # result是从数据库查询回来的用户信息
    # result有两种结果：1、None  2、{"user_id":1,"username":xxx,"password":"111"}
    return result

# 2、根据用户名和密码添加数据的函数
def add_user(username,password):
    sql = "insert into sys_user (username,password) values (%s,%s)"
    cur = conn.cursor()
    cur.execute(sql, [username,password])
    conn.commit()

# 3、根据用户id查询当前用户的AI助手聊天信息的函数
def query_message_by_user_id(user_id):
    sql = "select * from chat_message where user_id = %s order by message_time asc"
    cur = conn.cursor()
    cur.execute(sql, [user_id])
    # 字典类型的列表[{},{},{}]
    list = cur.fetchall()
    return list

def add_message(user_id, message,role,message_time):
    sql="insert into chat_message (user_id, message,role,message_time) values (%s,%s,%s,%s)"
    cursor=conn.cursor()
    cursor.execute(sql, (user_id, message,role,message_time))
    conn.commit()

def change_password(username,password):
    sql="update sys_user set password = %s where username= %s"
    cursor=conn.cursor()
    cursor.execute(sql, (password,username))
    conn.commit()
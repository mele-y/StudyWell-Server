from flask import Flask
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)


# 数据库连接
def connection():
    global conn
    conn = pymysql.Connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='gehao',
        db='demo_01',
        charset='utf8'
    )


connection()


@app.route('/')
def hello_world():
    return '新的服务器首页！'


@app.route('/register/<name>/<password>')
def register(name, password):
    cursor = conn.cursor()
    try:
        insert_sql_1 = "insert into study_user(username, password) values ('%s', '%s')" % (name, password)
        cursor.execute(insert_sql_1)
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()

    sql = "select * from study_user"
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        username = row[0]
        password = row[1]
        print("username: %s , password: %s" % (username, password))
    cursor.close()
    conn.close()
    return "注册成功: %s" % name


if __name__ == '__main__':
    app.run(debug=True)

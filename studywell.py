import sqlite3
import json
from flask import Flask, redirect, request

app = Flask(__name__)


@app.route("/index")
def index():
    return "<h1 style='color:red'>flaskSql Hello World</h1>"


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        conn = sqlite3.connect("StudyWell.db")
        user_id_temp = str(request.form['user_id'])
        username_temp = str(request.form['username'])
        password_temp = str(request.form['password'])
        image_temp = str(request.form['image'])
        cursor = conn.cursor()
        user_list = cursor.execute("select * from user where user.username = ?", (username_temp,))
        user_list = user_list.fetchall()
        if len(user_list):
            ans = "the username has been registerd"
        else:
            cursor.execute('insert into user(username,password,user_id,image) values(?,?,?,?)',
                           (username_temp, password_temp, user_id_temp, image_temp))
            ans = "register sucessfully"
            conn.commit()
        cursor.close()
        conn.close()
        return ans
    else:
        return "GET"


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        conn = sqlite3.connect("StudyWell.db")
        username_temp = str(request.form['username'])
        password_temp = str(request.form['password'])
        cursor = conn.cursor()
        user = cursor.execute("select * from user where user.username = ?", [username_temp, ]).fetchall()
        if len(user) <= 0:
            status = '2'
            msg = 'user does not exist'
            data = []
        else:
            user_password = user[0][1]
            if password_temp == user_password:
                status = '1'
                msg = 'login success'
                book_list = cursor.execute("select * from book").fetchall()
                data = []
                for book in book_list:
                    book_info = {
                        "book_id": book[1],
                        "book_name": book[0],
                        "auther": book[2],
                        "publcation": book[3],
                        "book_description": book[4],
                        "publish_date": book[5],
                        "upload_date": book[6],
                    }
                    data.append(book_info)
            else:
                status = '3'
                msg = 'password error'
                data = []
        ans = {
            "status": status,
            "msg": msg,
            "data": data
        }

        cursor.close()
        conn.close()
        return ans
    else:
        return "GET"


@app.route('/upload_books', methods=['GET', 'POST'])
def upload_books():
    if request.method == 'POST':
        conn = sqlite3.connect("StudyWell.db")
        name_temp = str(request.form['name'])
        id_temp = str(request.form['id'])
        auther_temp = str(request.form['auther'])
        publisher_temp = str(request.form['publisher'])
        publish_time_temp = str(request.form['publish time'])
        cursor = conn.cursor()
        user_list = cursor.execute('insert into books(name, id, auther, publisher, publish time) values(?, ?, ?, ?, ?)',
                                   (name_temp, id_temp, auther_temp, publisher_temp, publish_time_temp))
        user_list = user_list.fetchall()
        ans = ""
        cursor.close()
        conn.close()
        return ans
    else:
        return "GET"


if __name__ == "__main__":
    app.run()
# books = {}
# for book in book_list:
#     book_temp = {
#         "book_id": book[1],
#     }
# start
# book_key = []
# book_value = []
# for book in book_list:
#     book_key.append(book[1])
#     book_value_temp = [book[0], book[2], book[3], book[4], book[5], book[6], book[7]]
#     book_value.append(book_value_temp)
# book_dict = dict(zip(book_key, book_value))
# end
# if len(book_list):
#     # print(type(json.dumps(book_dict, ensure_ascii=False)))
#     # ans = json.dumps(book_dict, ensure_ascii=False)
#     ans = "to be continued"
# else:
#     ans = "there is no book!"

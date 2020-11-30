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
        username_temp = str(request.form['username'])
        password_temp = str(request.form['password'])
        cursor = conn.cursor()
        user_list = cursor.execute("select * from user where user.username = ?", (username_temp,))
        user_list = user_list.fetchall()
        if len(user_list):
            ans = "the username has been registerd"
        else:
            cursor.execute('insert into user(username,password) values(?,?)', (username_temp, password_temp,))
            ans = "register sucessfully"
            conn.commit()
        cursor.close()
        conn.close()
        return ans
    else:
        return "GET"


@app.route('/getbooks', methods=['GET', 'POST'])
def getbooks():
    if request.method == 'POST':
        conn = sqlite3.connect("StudyWell.db")
        cursor = conn.cursor()
        book_list = cursor.execute("select * from book")
        book_list = book_list.fetchall()
        book_key = []
        book_value = []
        for book in book_list:
            book_key.append(book[1])
            book_value_temp = []
            book_value_temp.append(book[0])
            book_value_temp.append(book[2])
            book_value_temp.append(book[3])
            book_value_temp.append(book[4])
            book_value.append(book_value_temp)
        book_dict = dict(zip(book_key, book_value))
        if len(book_list):
            # print(book_list)
            # print(book_dict)
            # print(json.dumps(book_dict, ensure_ascii=False))
            print(type(json.dumps(book_dict, ensure_ascii=False)))
            ans = json.dumps(book_dict, ensure_ascii=False)
        else:
            ans = "there is no book!"
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

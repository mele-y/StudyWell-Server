import sqlite3
import json
from flask import Flask, redirect, request

app = Flask(__name__)

conn = sqlite3.connect("StudyWell.db")


@app.route("/index")
def index():
    return "<h1 style='color:red'>flaskSql Hello World</h1>"


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username_temp = str(request.form['username'])
        password_temp = str(request.form['password'])
        cursor = conn.cursor()
        user_list = cursor.execute("select * from user where user.username = ?", (username_temp,))
        user_list = user_list.fetchall()
        ans = ""
        if (len(user_list)):
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
        cursor = conn.cursor()
        user_list = cursor.execute("select * from user")
        user_list = user_list.fetchall()
        ans = ""
        if (len(user_list)):
            print(user_list)
            jsonArr = json.dumps(user_list, ensure_ascii=False)
            print(json.dumps(dict(user_list)))
            ans = "the username has been get!"
        cursor.close()
        conn.close()
        return ans
    else:
        return "GET"


@app.route('/upload_books', methods=['GET', 'POST'])
def getbooks():
    if request.method == 'POST':
        name_temp = str(request.form['name'])
        id_temp = str(request.form['id'])
        auther_temp = str(request.form['auther'])
        publisher_temp = str(request.form['publisher'])
        publish_time_temp = str(request.form['publish time'])
        cursor = conn.cursor()
        user_list = cursor.execute('insert into books(name, id, auther, publisher, publish time) '
                                   'values(?,?,?,?,?)', (name_temp, id_temp, auther_temp, publisher_temp, publish_time_temp))
        user_list = user_list.fetchall()
        ans = ""

        cursor.close()
        conn.close()
        return ans
    else:
        return "GET"


if __name__ == "__main__":
    app.run()

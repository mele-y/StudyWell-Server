import sqlite3
import json
from flask import Flask, redirect, request, jsonify
import os
from werkzeug.utils import secure_filename
app = Flask(__name__)
import time

@app.route("/index")
def index():
    return "<h1 style='color:red'>flaskSql Hello World</h1>"


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


@app.route('/upload_book/', methods=['GET', 'POST'])
def upload_book():
    if request.method == 'POST':
        conn = sqlite3.connect("StudyWell.db")
        book_name= str(request.form['book_name'])
        author = str(request.form['author'])
        publication = str(request.form['publication'])
        description = str(request.form['description'])
        publish_date = str(request.form['publish_date'])
        book_file = request.files['book_file']
        file_type = str(secure_filename(book_file.filename)).split('.')[-1]
        cursor = conn.cursor()
        id_list = cursor.execute("select book_id from book order by book_id desc ").fetchall()
        max_id = id_list[0][0]+1
        upload_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # path in server
        path ="/www/wwwroot/book/"+str(max_id)+"_"+book_name+"."+file_type
        # test in localhost
        #path = str(max_id)+"_"+book_name+"."+file_type
        book_file.save(path)
        cursor.execute("insert into book(book_name,book_id,author,publication,publish_date,book_description,book_location,upload_date)"
                       "values (?,?,?,?,?,?,?,?)",[book_name,max_id,author,publication,publish_date,description,path,upload_date,])
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify(msg="upload successfully",code =1 )
    else:
        return "GET"


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username_register = request.form['username']
        password_register = request.form['password']
        userphoto_register =request.files['user_photo']
        connection =sqlite3.connect("StudyWell.db")
        cursor =connection.cursor()
        user_list = cursor.execute("select * from user where user.username = ?",[username_register,]).fetchall()
        msg = ""
        code = 0
        if len(user_list) == 0:
            file_type = str(secure_filename(userphoto_register.filename)).split('.')[-1]
            #path in server
            path = "/www/wwwroot/user_photo/"+str(username_register)+"."+file_type
            #test in localhost
            #path =  str(username_register) + "." + file_type
            userphoto_register.save(path)
            code = 1
            msg = "register successfully"
            cursor.execute("insert into user(username,password,image) values(?,?,?)",[username_register,password_register,path,])
            connection.commit()
        else:
            code = 0
            msg = "user  already exists"
        cursor.close()
        connection.close()
        return jsonify(code =code,msg = msg )
    else:
        return "only accept post method"

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

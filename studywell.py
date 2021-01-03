import sqlite3
import json
from flask import Flask, redirect, request, jsonify, send_file, send_from_directory, render_template, url_for
import os
import shutil
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
            code = 2
            msg = 'user does not exist'
            data = []
        else:
            user_password = user[0][1]
            if password_temp == user_password:
                code = 1
                msg = 'login success'
                book_list = cursor.execute("select * from book").fetchall()
                data = []
                i = 0
                for book in book_list:
                    if i < 10:
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
                        i += 1
                    else:
                        break
            else:
                code = 3
                msg = 'password error'
                data = []
        cursor.close()
        conn.close()
        return jsonify(code=code, msg=msg, data=data)
    else:
        return "GET"


@app.route('/upload_book', methods=['GET', 'POST'])
def upload_book():
    if request.method == 'POST':
        conn=sqlite3.connect("StudyWell.db")
        book_name = str(request.form['book_name'])
        author = str(request.form['author'])
        publication = str(request.form['publication'])
        description = str(request.form['description'])
        publish_date = str(request.form['publish_date'])
        book_file = request.files['book_file']
        book_cover = request.files['book_cover']
        category = str(request.form['category'])
        upload_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        file_type = str(secure_filename(book_file.filename)).split('.')[-1]
        cursor = conn.cursor()
        id_list =cursor.execute("select book_id from temporary order by book_id desc").fetchall()
        if len(id_list)!=0:
           max_id = id_list[0][0]+1
        else:
           max_id = 1
        book_cover_type = str(secure_filename(book_cover.filename)).split('.')[-1]
        cover_path ="/www/wwwroot/test/temporary/book_cover/"+str(max_id)+"_"+book_name+"."+book_cover_type
        book_path = "/www/wwwroot/test/temporary/bookfile/"+str(max_id)+"_"+book_name+"."+file_type
        book_file.save(book_path)
        book_cover.save(cover_path)
        cursor.execute("insert into temporary(book_name,book_id,author,publication,publish_date,book_description,upload_date,book_path,cover_path,category) "
                       "values (?,?,?,?,?,?,?,?,?,?)",[book_name,max_id,author,publication,publish_date,description,upload_date,book_path,cover_path,category])
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify(msg="等待审核", code=1)
    else:
        return "GET"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username_register = request.form['username']
        password_register = request.form['password']
        userphoto_register = request.files['user_photo']
        connection = sqlite3.connect("StudyWell.db")
        cursor = connection.cursor()
        user_list = cursor.execute("select * from user where user.username = ?", [username_register, ]).fetchall()
        if len(user_list) == 0:
            file_type = str(secure_filename(userphoto_register.filename)).split('.')[-1]
            # path in server
            path = "/www/wwwroot/user_photo/" + str(username_register) + "." + file_type
            # test in localhost
            # path =  str(username_register) + "." + file_type
            userphoto_register.save(path)
            code = 1
            msg = "register successfully"
            cursor.execute("insert into user(username,password,image) values(?,?,?)",
                           [username_register, password_register, path, ])
            connection.commit()
        else:
            code = 0
            msg = "user  already exists"
        cursor.close()
        connection.close()
        return jsonify(code=code, msg=msg)
    else:
        return "only accept post method"


@app.route('/query', methods=['GET', 'POST'])
def query():
    if request.method == 'GET':
        query_info = str(request.args["info"])
        page = int(request.args['page'])
        category = str(request.args["category"])
        connection = sqlite3.connect("StudyWell.db")
        cursor = connection.cursor()
        pages = 0
        # cursor.execute("ALTER TABLE book ADD COLUMN category TEXT;")
        s = "select * from book where " \
            "(book.book_name like '%" + query_info + \
            "%' or book.author like '%" + query_info + \
            "%' or book.publication like '%" + query_info + \
            "%' or book.publish_date like '%" + query_info + \
            "%' or book.book_description like '%" + query_info + \
            "%' or book.book_description like '%" + query_info + "%') "
        if len(category) != 0:
            book_list = cursor.execute(s + "and book.category = ? order by upload_date desc", [category, ]).fetchall()
        else:
            book_list = cursor.execute(s + "order by upload_date desc").fetchall()
        data = {}
        if len(book_list) == 0:
            code = 0
            msg = "cant find any books"
            data_book = []
            connection.commit()
        else:
            code = 1
            msg = 'query success'
            data_book = []
            pages = int(len(book_list) / 10) + 1 if(len(book_list) % 10 != 0) else len(book_list) / 10
            start = (page - 1) * 10
            end = len(book_list) if(page == pages) else (page - 1) * 10 + 10
            for i in range(start, end):
                book_info = {
                    "book_name": book_list[i][0],
                    "book_id": book_list[i][1],
                    "author": book_list[i][2],
                    "publication": book_list[i][3],
                    "publish_date": book_list[i][4],
                    "book_description": book_list[i][5],
                    "book location": book_list[i][6],
                    "upload_date": book_list[i][7],
                    "book_cover_url": book_list[i][8]
                }
                data_book.append(book_info)
        cursor.close()
        connection.close()
        data["page"] = page
        data["pages"] = pages
        data["data_book"] = data_book
        return jsonify(code=code, msg=msg, data=data)
    else:
        return "only accept get method"


@app.route("/download_book")
def download_book():
        book_id = request.args.get('book_id')
        conn =sqlite3.connect("StudyWell.db")
        cursor =conn.cursor()
        path_list = cursor.execute("select book_location from book where book.book_id = ?",[book_id,]).fetchall()
        path = path_list[0][0]
        file_dir,str,file_name = path.rpartition("/")
        cursor.close()
        conn.close()
        return send_from_directory(file_dir,file_name,as_attachment = True)

@app.route("/manage")
def manage():
    conn = sqlite3.connect("StudyWell.db")
    cursor = conn.cursor()
    book_list = cursor.execute("select * from book").fetchall()
    temporary_list = cursor.execute("select * from temporary").fetchall()
    cursor.close()
    conn.close()
    return render_template('admin.html',book_list=book_list,temporary_list=temporary_list)

@app.route("/delete/<int:book_id>",methods=['POST'])
def delete_book(book_id):
    conn=sqlite3.connect("StudyWell.db")
    print(book_id)
    cursor=conn.cursor()
    cursor.execute("delete from book where book.book_id = ?",[book_id,])
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('manage'))

@app.route("/delete_temporary/<int:id>",methods=['POST'])
def delete_temporary(id):
    conn=sqlite3.connect("StudyWell.db")
    cursor=conn.cursor()
    item_list = cursor.execute("select * from temporary where temporary.book_id = ? ",[id,]).fetchall()
    item = item_list[0]
    book_path = item[8]
    cover_path = item[9]
    if os.path.exists(book_path):
        os.remove(book_path)
    if os.path.exists(cover_path):
        os.remove(cover_path)
    cursor.execute("delete from temporary where temporary.book_id = ?",[id,])
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('manage'))
    
    
@app.route("/accept_temporary/<int:id>",methods=['POST'])
def accept_temporary(id):
    conn = sqlite3.connect("StudyWell.db")
    cursor = conn.cursor()
    item_list = cursor.execute("select * from temporary where temporary.book_id = ?",[id,]).fetchall()
    item = item_list[0]
    cursor.execute("delete from temporary where temporary.book_id = ?",[id,])
    book_name =item[0]
    old_id =item[1]
    author = item[2]
    publication =item[3]
    publish_date = item[4]
    book_description = item[5]
    upload_date = item[6]
    category = item[7]
    book_path = item[8]
    cover_path = item[9]
    id_list = cursor.execute("select book_id from book order by book_id desc").fetchall()
    if len(id_list) != 0:
        max_id = id_list[0][0] + 1
    else:
        max_id = 1
    bookfile_type = book_path.split('.')[-1]
    covertype = cover_path.split('.')[-1]
    shutil.move(book_path,"/www/wwwroot/book")
    shutil.move(cover_path,"/www/wwwroot/test/static/book_cover")
    path="/www/wwwroot/book/"+str(max_id)+"_"+book_name+"."+bookfile_type
    book_cover_URL="http://121.196.150.190/static/book_cover/"+str(max_id)+"_"+book_name+"."+covertype
    os.rename("/www/wwwroot/book/"+str(old_id)+"_"+book_name+"."+bookfile_type,path)
    os.rename("/www/wwwroot/test/static/book_cover/"+str(old_id)+"_"+book_name+"."+covertype,"/www/wwwroot/test/static/book_cover/"+str(max_id)+"_"+book_name+"."+covertype)
    cursor.execute(
        "insert into book(book_name,book_id,author,publication,publish_date,book_description,book_location,upload_date,book_cover_url,category)"
        "values (?,?,?,?,?,?,?,?,?,?)",
        [book_name, max_id, author, publication, publish_date, book_description, path, upload_date, book_cover_URL,
         category])
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('manage'))
    
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
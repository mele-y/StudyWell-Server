import sqlite3
from flask import Flask,redirect,request
app = Flask(__name__)

@app.route("/index")
def index():
    return "<h1 style='color:red'>flaskSql Hello World</h1>"
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username_temp = str(request.form['username'])
        password_temp = str(request.form['password'])
        conn = sqlite3.connect("StudyWell.db")
        cursor = conn.cursor()
        user_list = cursor.execute("select * from user where user.username = ?",(username_temp,))
        user_list = user_list.fetchall()
        ans = ""
        if( len( user_list ) ):
            ans = "the username has been registerd"
        else:
            cursor.execute('insert into user(username,password) values(?,?)',(username_temp,password_temp,))
            ans = "register sucessfully"
            conn.commit()
        cursor.close()
        conn.close()
        return ans
    else:
        return "GET"

if __name__ == "__main__":
    app.run()
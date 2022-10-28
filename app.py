# !/usr/bin/python
# coding:utf-8

from flask import Flask, request, redirect, render_template, session, url_for
import mysql.connector

app = Flask(__name__,static_folder="static",static_url_path="/")
app.secret_key="any string but secret"



mydb = mysql.connector.connect(
        host = "localhost",
        port = 3306,
        user = "root",
        database = "db_1028",
        password = " ",
        charset = "utf8"
        )

#處理 GET 方法處理路徑 / 的對應函式
@app.route("/")
def index():
    return render_template("index.html")

#註冊
@app.route("/signup", methods=["POST"])
def signup():
    #取得輸入資料的方法
    name=request.form["name"]
    account=request.form["account"]
    password=request.form["password"]
    sql = """
    SELECT * FROM member WHERE account = %s;
    """
    data = (account, )
    #建立操作游標
    mycursor = mydb.cursor()
    #執行語法
    mycursor.execute(sql, data)
    row = mycursor.fetchone()

    #註冊失敗，重新輸入
    
    if name == "" or account == "" or password == "":
        return redirect(url_for("error", message = "請重新輸入"))
    #註冊失敗，導到失敗頁
    elif row:
        return redirect(url_for("error", message = "帳號已經被註冊"))
    #註冊成功，回首頁
    else:
        sql = """
        INSERT INTO member (name, account, password) VALUES (%s, %s, %s)
            """
        data = (name, account, password)
        mycursor.execute(sql, data)
        mydb.commit()
        return redirect("/")

@app.route("/signin", methods=["POST"])
def signin():
    account=request.form["account"]
    password=request.form["password"]
    sql = """
        SELECT * FROM member WHERE account = %s AND password = %s
    """
    data = (account, password)
    mycursor = mydb.cursor()
    mycursor.execute(sql, data)
    row = mycursor.fetchone()

    if row:
        session["name"] = row[1]
        session["account"] = account
        session["password"] = password
        return redirect("/member")
    elif account == "" or password == "":
        return redirect(url_for("error", message = "請確認後重新填寫"))
    else:
        return redirect(url_for("error", message = "帳號或密碼輸入錯誤"))



@app.route("/member")
def member():
    if "account" in session:
        #將名字取出放到變數內
        name = session["name"]
        return render_template("member.html", name = name)
    else:
        return redirect("/")



@app.route("/error")
def error():
    error=request.args.get("message", "")
    return render_template("error.html", message = error)

@app.route("/signout")
def signout():
    session.pop("account", None)
    return redirect('/')

    """
    session.pop("account", None)
    # Session class is a wrapper around a python Dict
    # pop(key[, default])
    # If key is in the dictionary, remove it and return its value, else return default. If default is not given and key is not in the dictionary, a KeyError is raised.
    """



app.run(port=3000)

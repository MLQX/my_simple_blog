# from flask import Flask

from config import *


app = Flask(__name__)

app.secret_key = SECRET_KEY


# 初始数据库,用数据表
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('create_table.sql') as f:
            # print(type(f.read()))
            print(f.read())
            db.cursor().executescript(str(f.read(),encoding='utf-8'))
        db.commit()




# 链接数据库
def connect_db():
    return sqlite3.connect(DATABASE)


@app.before_request
def before_request():
    g.db = connect_db()

@app.after_request
def after_request(response):
    g.db.close()
    # print(type (response))
    return response



@app.route("/init_db")
def init():
    init_db()
    flash('数据库初始化成功')
    return redirect(url_for("show_entries"))

@app.route('/')
def show_entries():
    # init_db()

    cur = g.db.execute("select title, content from entries order by id desc")

    entries = [dict(title=row[0],content=row[1]) for row in cur.fetchall()]


    # if request.method == 'POST':
    #     return redirect(url_for("add_entry"))

    return render_template("show_entries.html",entries=entries)


@app.route("/add",methods=['POST'])
def add_entry():
    # 添加文章
    # 查看登录状态，如果已登录， 向数据库写入表单，重定向到 '/';  未登录提示

    # 如果未登录则提示 ，logged_in 表登录状态
    if not session.get("logined_in"):
        flash("未登录")
        abort(401)
    g.db.execute("insert into entries(title, content) values (?,?)", [request.form.get('title'),request.form.get('content')])

    g.db.commit()
    # 向数据库写入表单，重定向到'/'
    return redirect(url_for("show_entries"))



# 登录
@app.route("/login", methods=['GET','POST'])
def login():
    # if request.method == 'POST':
        # if request.form.get("username") == USERNAME and request.form.get('password') == PASSWORD:
        #     # 姓名密码验证通过
        #     # 置标志量 为 True
        #     session['logined_in'] = True
        #     return redirect(url_for("index"))
    # return render_template("login.html")
    error = None
    if request.method == 'POST':
        if request.form['username'] != USERNAME:
            error = 'Invalid username'
        elif request.form['password'] != PASSWORD:
            error = 'Invalid password'
        else:
            session['logined_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries')) ####
    session.pop("logined_in",None)  # 删除
    return render_template('login.html', error=error)





# 登出
@app.route("/logout")
def logout():
    session.pop("logined_in",None)
    flash("You are logged out")
    return redirect(url_for('show_entries'))


if __name__ == '__main__':

    app.run()

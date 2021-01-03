from flask import Flask, request
from flask import render_template, redirect, url_for, session, g, flash , make_response
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
import os
import jiagu
from datetime import timedelta, datetime
import pymysql
from flask_bootstrap import Bootstrap
from flask_paginate import Pagination, get_page_parameter
from flask_mail import Mail, Message
import config
from flask_admin import Admin
from dataclasses import dataclass
from models import User, Workers, db, UserLog
from forms import WorkersForm, RegistForm, LoginForm, File
from functools import wraps
from flask_login import current_user, login_user, LoginManager, login_required, login_manager
from sqlalchemy import and_
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_uploads import UploadSet, IMAGES, configure_uploads, patch_request_class
from PIL import Image

app = Flask(__name__, static_url_path="/")
app.config.from_object(config)
bootstrap = Bootstrap(app)
mail = Mail(app)
mail.init_app(app)
admin = Admin(app, name=u'Python数据管理')
db.init_app(app)
login_manager = LoginManager(app)
login_manager.init_app(app)


#实例化一个file对象  photos与PHOTOS要对应
file = UploadSet('photos',IMAGES)

#将 app 的 config 配置注册到 UploadSet 实例 file
configure_uploads(app,file)
#限制上传文件的大小   size=None不采用默认size=64*1024*1024
patch_request_class(app,size=None)


#用户加载功能注册函数
@app.before_request
def before_request():
    g.user = None
    if 'username' in session:
        users = User.query.all()
        user = [u for u in users if u.username == session['username']]
        g.user = user

@login_manager.user_loader
def load_user(username):
    print(username)
    return User.get(username)

#用户注册
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistForm()
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        repassword = request.form['repassword']
        if User.query.filter_by(username=username).all():
            error = '用户名已存在'
            return render_template('register.html', form=form, error=error)
        if username is None:
            error = 'Invalid username'
        if password != repassword:
            error = '密码不一致'
            return render_template('register.html', form=form, error=error)
        else:
            form.validate_on_submit()
            data = form.data
            user = User(
                username = data["username"],
                password = generate_password_hash(data["password"]),
                addtime = datetime.now()
            )
            db.session.add(user)
            db.session.commit()
            flash("注册成功！", "OK")
            return redirect(url_for('login'))
    return render_template("register.html", form=form, error=error)


#用户登录
@app.route("/login", methods=['get','POST'])
def login():
    error = None
    form = LoginForm()
    if request.method == 'POST':
        # 登录操作
        # 获取表单中的数据
        username = request.form.get("username")
        password = request.form.get("password")
        #在数据库中查找数据
        user = User.query.filter_by(username=request.form['username']).first()
        #用户名和密码匹配成功时
        if user is None:
            error = '请输入正确的用户名'
        elif password is None:
            error = '密码错误请重新输入'
        elif user.check_pwd(password):                  #哈希密码验证，正确为True，否则为false
            session['username'] = request.form['username']
            session['id'] = user.id
            flash('登陆成功')
            return redirect(url_for('index'))
        else:
            error = "账号或者密码不对"

    return render_template("login.html", form=form, error=error, session=session)


@app.route("/")
def index():
    if not g.user:
        return redirect('login')
    PER_PAGE = 10                                                                          #每页显示条数
    total = db.session.query(Workers).count()                                             #总共的数据库单列数据条数
    page = request.args.get(get_page_parameter(),type=int,default=1)                      #获取页码，默认为第一页
    start = (page - 1) * PER_PAGE                                                         #每一页开始位置
    end = start + PER_PAGE                                                                #每一页结束位置
    pagination = Pagination(bs_version=3, page=page, total=total)                         #bootstr的版本， 默认为2
    workers = db.session.query(Workers).slice(start, end)                                 #对数据展示页切割数据

    context = {
        'pagination': pagination,
        'workers': workers
    }
    return render_template("index.html", **context, )

#退出登录
@app.route("/logout",methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    flash("退出成功")
    return redirect(url_for('login'))


#表格添加字段
@app.route("/profile", methods=['GET','POST'])
def profile():
    if not g.user:
        return redirect(url_for('login'))

    workers_form = WorkersForm()
    if workers_form.validate_on_submit():
        positionName = workers_form.positionName.data
        companyFullName = workers_form.companyFullName.data
        companySize = workers_form.companySize.data
        financeStage = workers_form.financeStage.data
        secondType = workers_form.secondType.data
        salary = workers_form.financeStage.data
        workYear = workers_form.workYear.data
        education = workers_form.workYear.data
        obj = Workers(positionName=positionName, companyFullName=companyFullName, companySize=companySize,financeStage=financeStage, secondType=secondType, salary=salary, workYear=workYear, education=education)

        print(obj.education)
        db.session.add(obj)             #添加数据到数据库
        db.session.commit()             #确认提交数据
        return '提交成功'
    else:
        if request.method == 'POST':
            return '验证未通过'
    return render_template("profile.html", form=workers_form)


#发送文本
@app.route('/email_send_charactor/')
def email_send_charactor():
    # 发送邮件的标题、接收方、内容
    message = Message(subject="hello flask-mail", recipients=['wyh17702296834@163.com'], body='flask-mail测试代码')
    try:
        mail.send(message)
        return '发送成功！请注意查收！'
    except Exception as E:
        print(E)
        return '发送失败！'

#发送一个html
@app.route('/email_send_html/')
def email_send_html():
    message = Message(subject='hello flask-mail',recipients=['1417766861@qq.com'])
    try:
        #发送渲染一个模板
        message.html = render_template('email_temp.html')
        mail.send(message)
        return '发送成功，请注意查收~'
    except Exception as e:
        print(e)
        return '发送失败'

#发送附带附件的邮件
@app.route('/email_send_attach/')
def email_send_attach():
    message = Message(subject='hello flask-mail',recipients=['1417766861@qq.com'],body='我是一个附件邮件')
    try:
        # message.attach邮件附件添加
        # 方法attach(self,
        #        filename=None,
        #        content_type=None,
        #        data=None,
        #        disposition=None,
        #        headers=None):

        with open(filename,'rb') as fp:
            message.attach("test.jpg", "image/jpg", fp.read())
        mail.send(message)
        return '发送成功，请注意查收~'
    except Exception as e:
        print(e)
        return '发送失败'

#文件上传
#生成随机名称函数
def new_name(shuffix, length=32):
    import string, random
    myStr = string.ascii_letters + '010020'
    newName = ''.join(random.choice(myStr) for i in range(length))
    return newName+shuffix

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = File()
    img_url = None
    #验证数据
    if form.validate_on_submit():
        shuffix = os.path.splitext(form.file.data.filename)[-1]
        newName = new_name(shuffix=shuffix)
        file.save(form.file.data, name=newName)
        img_url = file.url(newName)
    return render_template('boot_upload.html', newName=img_url, form=form)


if __name__ == '__main__':
    app.run(port=5050, debug=True)
    # 设置静态文件缓存过期时间
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
    # 也可以这样写：
    # app.send_file_max_age_default = timedelta(seconds=1)



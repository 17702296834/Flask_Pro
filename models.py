from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash


# 生成连接数据库的对象
db = SQLAlchemy()


#解耦数据库，数据库字段、类型
#后台登录管理员字段
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100),nullable=False, unique=True)
    password = db.Column(db.String(100),nullable=False)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    userlogs = db.relationship("UserLog", backref="user")      #会员日志外键关联

    def __repr__(self):
        return "<User %r>" % self.username
        # return "user = %s" %self.username

    def check_pwd(self,password):
        return check_password_hash(self.password, password)


#登录日志表
class UserLog(db.Model):
    __tablename__ = "userlog"                                               #表名
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)        # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))               # 所属会员
    ip = db.Column(db.String(100))                                          # 登录IP
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)      # 登录时间；

    def __repr__(self):
        return "<UserLog %r>" % self.id


#业务端数据库数据类型
class Workers(db.Model):
    __tablename__ = 'python'
    __table_args__ = {'mysql_engine': 'InnoDB'}               #支持事务操作和外键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    positionName = db.Column(db.String(40))
    companyFullName = db.Column(db.String(30))
    companySize = db.Column(db.String(60))
    financeStage = db.Column(db.String(30))
    secondType = db.Column(db.Text)
    salary = db.Column(db.String(30))
    workYear = db.Column(db.String(30))
    education = db.Column(db.String(20))
    lastLogin = db.Column(db.DateTime, default=datetime.now())


# if __name__ == '__main__':
#     db.create_all()
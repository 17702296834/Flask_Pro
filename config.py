# encoding:utf-8
import os

# 数据库
HOST = '39.106.81.151'
PORT = '3306'
DATABASE = 'stats_gov_data'
USERNAME = 'root'
PASSWORD = 'WYH123wyh123'

# DB_URI = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (DB_USERNAME,DB_PASSWORD,DB_HOST,DB_PORT,DB_NAME)
DB_URI = 'mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8mb4'.format(username=USERNAME, password=PASSWORD, host=HOST, port=PORT, db=DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False


# 邮箱
MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = "1520637008@qq.com"
MAIL_PASSWORD = "wjqgytsdnodebabj"            #授权码
MAIL_DEFAULT_SENDER = "1520637008@qq.com"



# MAIL_SERVER	localhost	电子邮件服务器的主机名或IP地址
# MAIL_PORT	587	电子邮件服务器的端口
# MAIL_USE_TLS	False	启用传输层安全协议
# MAIL_USE_SSL	False	启用安全套接层协议
# MAIL_USERNAME	None	邮件账户的用户名
# MAIL_PASSWORD	None	邮件账户的密码

# UPLOADED_PHOTOS_URL = 'http://127.0.0.1:5050/static/uploads/'
SECRET_KEY = '1237c77382064196b8a97dd40191cbfa'
#文件上传大小
MAX_CONTENT_LENGTH = 1024*1024*64             #64兆
#允许上传的后缀名,放在配置文件
# ALLOWED_EXTENSIONS = ['jpg','jpeg','png','gif','txt','xlsx','docx']
#配置文件上传的路径
UPLOADED_PHOTOS_DEST = os.getcwd() + '/static/uploads'
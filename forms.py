from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, IntegerField, TextField, PasswordField
from wtforms.validators import DataRequired, InputRequired, Length, EqualTo, Email, ValidationError
from wtforms import FileField
from flask_wtf.file import FileAllowed, FileRequired

#注册表单
class RegistForm(FlaskForm):
    username = StringField(label="昵称", validators=[DataRequired("请输入昵称!")], description="昵称", render_kw={"class": "form-control input-lg", "placeholder": "在这里写昵称！"})
    password = PasswordField(label="密码", validators=[DataRequired("请输入密码!")], description="密码", render_kw={"class": "form-control input-lg", "placeholder": "在这里填写密码！"})
    repassword = PasswordField(label="确认密码", validators=[DataRequired("请输入密码!"), EqualTo('password', message="两次输入密码不一致！")], description="确认密码", render_kw={"class": "form-control input-lg", "placeholder": "再次输入密码！"})
    submit = SubmitField(label="提交注册", render_kw={"class": "btn btn-lg btn-success btn-block"})

    def validate_name(self,field):
        username = field.data
        user = User.query.filter_by(username=username).count()
        if user==1:
            raise ValidationError("昵称已经存在！")


#后端登录注册
class LoginForm(FlaskForm):
    username = StringField(label="账户", validators=[DataRequired("前请输入账户！")], description="账户", render_kw={"class": "form-control input-log", "placeholder": "在这里填写账户！"})
    password = PasswordField(label="密码", validators=[DataRequired("请输入密码!")], description="密码", render_kw={"class": "form-control input-lg", "placeholder": "在这里填写密码！"})
    submit = SubmitField(label="登录", render_kw={"class": "btn btn-lg btn-success btn-block"})


#业务端数据提交列表
class WorkersForm(FlaskForm):
    positionName = StringField(label='公司职称:', validators=[InputRequired(message='请输入公司职称')])
    companyFullName = StringField(label='公司名称:', validators=[InputRequired(message='请输入公司名称')])
    companySize = StringField(label='公司大小:', validators=[InputRequired(message='请输入公司大小')])
    financeStage = StringField(label='融资情况:', validators=[InputRequired(message='公司大小')])
    secondType = TextField(label='职位名称:', validators=[InputRequired(message='融资情况')])
    salary = StringField(label='薪资范围:', validators=[InputRequired(message='薪资范围')])
    workYear = StringField(label='工作年限:', validators=[InputRequired(message='工作年限')])
    education = StringField(label='职称级别:', validators=[InputRequired(message='职称级别')])
    submit = SubmitField(label='提交数据')


class File(FlaskForm):
    file = FileField('文件上传', validators=[FileRequired(message='你还没有上传文件'),FileAllowed(['jpg','jpeg','png','gif','txt','xlsx','docx'], message='只能上传图片、文本、Word、Excel')])
    submit = SubmitField('上传')

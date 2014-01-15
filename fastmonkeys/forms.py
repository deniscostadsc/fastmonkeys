from wtforms import Form, TextField, PasswordField, DateField
from wtforms.validators import Required


class RegisterForm(Form):
    name = TextField(u'name', validators=[Required()])
    email = TextField(u'email', validators=[Required()])
    password = PasswordField('password', validators=[Required()])
    date_of_birth = DateField('date_of_birth', format='%m/%d/%Y', validators=[Required()])

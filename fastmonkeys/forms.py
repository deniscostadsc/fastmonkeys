from wtforms import Form, TextField, PasswordField, DateField
from wtforms.validators import Required, ValidationError

from fastmonkeys.models import Monkey


class RegisterForm(Form):
    name = TextField(u'name', validators=[Required()])
    email = TextField(u'email', validators=[Required()])
    password = PasswordField('password', validators=[Required()])
    date_of_birth = DateField('date_of_birth', format='%m/%d/%Y', validators=[Required()])

    def validate_email(self, field):
        if Monkey.query.filter(Monkey.email == self.email.data).count() != 0:
            raise ValidationError('This email is already registered!')

import sys
from random import choice
from datetime import date

from sqlalchemy import Column, Integer, String, Date
from werkzeug import generate_password_hash, check_password_hash

from fastmonkeys.database import Base

if sys.version_info[0] == 3:
    unicode = str
    from string import digits, ascii_letters as letters
else:
    from string import digits, letters


# this way I can mock today 8D
def today():
    return date.today()


class Monkey(Base):
    __tablename__ = 'monkey'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(120), unique=True)
    date_of_birth = Column(Date)
    password = Column(String(80))
    salt = Column(String(1))

    def __init__(self, name, email, date_of_birth, password):
        self.name = name
        self.email = email
        self.date_of_birth = date_of_birth
        self.set_password(password)

    @property
    def age(self):
        return int((today() - self.date_of_birth).days / 365)

    def set_password(self, password):
        salt_characters = letters + digits
        self.salt = choice(salt_characters)
        self.password = generate_password_hash(password + self.salt)

    def check_password(self, password):
        return check_password_hash(self.password, password + self.salt)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '%s(name="%s", email="%s", date_of_birth="%s", password="%s")' % (
            self.__class__.__name__,
            self.__dict__['name'],
            self.__dict__['email'],
            self.__dict__['date_of_birth'],
            self.__dict__['password']
        )

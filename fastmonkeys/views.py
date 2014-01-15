from flask import render_template, redirect, url_for, request

from fastmonkeys import app
from fastmonkeys.forms import RegisterForm
from fastmonkeys.models import Monkey
from fastmonkeys.database import db_session


@app.route('/')
def index():
    return 'Hello World!'


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate():
        monkey = Monkey(
            form.name.data,
            form.email.data,
            form.date_of_birth.data,
            form.password.data
        )
        db_session.add(monkey)
        db_session.commit()
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

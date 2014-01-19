from flask import render_template, redirect, url_for, request
from flask_login import login_user, logout_user, login_required

from fastmonkeys import app
from fastmonkeys.forms import RegisterForm, LoginForm
from fastmonkeys.models import Monkey
from fastmonkeys.database import db_session


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'email' in request.form:
        monkey = Monkey.query.filter(Monkey.email == request.form.get('email')).first()
        if monkey is not None:
            if monkey.check_password(request.form.get('password')):
                login_user(monkey)
                return redirect(url_for('register'))
    form = LoginForm(request.form)
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        monkey = Monkey(
            form.name.data,
            form.email.data,
            form.date_of_birth.data,
            form.password.data
        )
        db_session.add(monkey)
        db_session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

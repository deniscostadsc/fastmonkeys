from datetime import datetime
from math import ceil

from flask import abort, render_template, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required

from fastmonkeys import app
from fastmonkeys.forms import RegisterForm, LoginForm, EditProfileForm
from fastmonkeys.models import Monkey
from fastmonkeys.database import db_session

per_page = 10


@app.errorhandler(404)
def _404(error):
    return render_template('404.html'), 404


@app.errorhandler(401)
def _401(error):
    return render_template('401.html'), 401


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


@app.route('/monkeys/<monkey_id>/')
@login_required
def profile(monkey_id):
    monkey = Monkey.query.get(monkey_id)
    if monkey is None:
        abort(404)
    return render_template('profile.html', monkey=monkey)


@app.route('/monkeys/')
@login_required
def list():
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1

    monkeys = Monkey.query.limit(per_page).offset((page - 1) * per_page).all()
    if not monkeys and page != 1:
        abort(404)

    total = len(Monkey.query.all())

    pages = int(ceil(total / float(per_page)))

    has_next = pages > page
    previous_page = page - 1
    has_previous = page > 1
    next_page = page + 1

    return render_template(
        'list.html',
        monkeys=monkeys,
        has_previous=has_previous,
        has_next=has_next,
        next_page=next_page,
        previous_page=previous_page
    )


@app.route('/friend/<monkey_id>/')
@login_required
def friend(monkey_id):
    monkey = current_user
    friend = Monkey.query.get(monkey_id)
    monkey.friends.append(friend)
    db_session.add(monkey)
    db_session.commit()
    return redirect(url_for('list'))


@app.route('/unfriend/<monkey_id>/')
@login_required
def unfriend(monkey_id):
    monkey = current_user
    friend = Monkey.query.get(monkey_id)
    monkey.friends.remove(friend)
    db_session.add(monkey)
    db_session.commit()
    return redirect(url_for('list'))


@app.route('/edit/', methods=['GET', 'POST'])
@login_required
def edit():
    monkey = current_user

    if request.method == 'POST':

        data = {}

        if request.form.get('email') and request.form.get('email') != monkey.email:
            data['email'] = request.form.get('email')

        form = EditProfileForm(**data)

        if form.validate():
            if request.form.get('name'):
                monkey.name = request.form.get('name')

            if request.form.get('email') and request.form.get('email') != monkey.email:
                monkey.email = request.form.get('email')

            if request.form.get('date_of_birth'):
                monkey.date_of_birth = datetime.strptime(request.form.get('date_of_birth'), '%m/%d/%Y').date()

            if request.form.get('password'):
                monkey.set_password(request.form.get('password'))

            db_session.add(monkey)
            db_session.commit()
    else:
        form = EditProfileForm(
            name=monkey.name,
            email=monkey.email,
            date_of_birth=monkey.date_of_birth
        )

    return render_template('edit.html', form=form)


@app.route('/delete/')
@login_required
def delete():
    monkey = current_user
    db_session.delete(monkey)
    db_session.commit()
    logout_user()
    return redirect(url_for('login'))

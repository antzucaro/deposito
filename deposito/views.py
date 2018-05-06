from flask import render_template, request, redirect, url_for
from flask import flash, g, session
from flask_login import login_user, logout_user
from wtforms import Form, StringField, TextAreaField, PasswordField
from wtforms import validators

from deposito import app, db, login_manager, pw_manager
from deposito.models import User


# forms (WTForms)
class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=3, max=25)])
    password = PasswordField('Password', [validators.Length(min=6, max=35)])


class RegisterForm(LoginForm):
    pw_confirm = PasswordField('Confirm Password', [validators.Length(min=6, max=35)])
    about = TextAreaField('About Yourself')
    email = StringField('Email',
                        [validators.Email(message="That doesn't appear to be a valid email!"),
                         validators.Optional()])


# regular views
@login_manager.user_loader
def load_user(id):
    try:
        user = db.session.query(User).filter(User.user_id == id).one()
        g.user = user
        session['id'] = user.user_id
    except:
        user = None

    return user


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data

        try:
            user = db.session.query(User).filter(User.username==username).one()
        except:
            user = User()
            user.password = ''

        if pw_manager.check(user.password, password):
            login_user(user)
            flash("Logged in successfully.")
            return redirect(url_for("main_index"))
        else:
            flash("Could not log you in. Please try again.")
            return redirect(url_for('login'))

    # not a POST, just showing the login form
    else:
        return render_template('login.jinja', form=form, next=url_for('main_index'))


@app.route('/logout')
def logout():
    logout_user()
    flash("You've successfully logged out!")

    return redirect(url_for("login"))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)

    # a registration request
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        password_confirm = form.pw_confirm.data
        email = form.email.data
        about = form.about.data

        err = False
        if password != password_confirm:
            err = True
            flash("Password and confirmation don't match!")

        users = db.session.query(User).filter(User.username==username).all()
        if len(users) > 0:
            err = True
            flash("Sorry, that username is already taken! Please pick another.")

        if err:
            return redirect(url_for("register"))

        hashed_password = pw_manager.encode(password)
        user = User()
        user.username = username
        user.password = hashed_password
        user.email = email
        user.about = about
        user.active_ind = True

        db.session.add(user)
        db.session.commit()

        login_user(user)

        flash("Account {0} created successfully.".format(user.username))

        return redirect(url_for("main_index", form=form))

    # not a POST, just showing the register form
    else:
        return render_template('register.jinja', form=form)


@app.route('/', methods=['GET'])
def main_index():
    return "Hello, world!"

import os
from cryptacular.bcrypt import BCRYPTPasswordManager
from deposito import *
from deposito.models import *
from deposito.util import md5sum
from flask import Flask, render_template, request, redirect, url_for
from flask import flash, g, session
from flask_login import login_required, login_user, logout_user
from werkzeug import secure_filename
from wtforms import Form, TextField, TextAreaField, PasswordField, FileField
from wtforms import validators

# forms (WTForms)
class LoginForm(Form):
    username     = TextField('Username', [validators.Length(min=3, max=25)])
    password     = PasswordField('Password', [validators.Length(min=6, max=35)])

class RegisterForm(LoginForm):
    pw_confirm   = PasswordField('Confirm Password', [validators.Length(min=6, max=35)])
    about        = TextAreaField('About Yourself')
    email        = TextField('Email',
            [validators.Email(message="That doesn't appear to be a valid email!"), validators.Optional()])

class SubmitMapForm(Form):
    name        = TextField('Name')
    pk3         = FileField(u'PK3')
    description = TextAreaField('Description', [validators.Optional()])
    version     = TextField('Version', [validators.Optional()])
    screenshot  = FileField(u'Primary Screenshot', [validators.Optional()])
    author      = TextField('Author', [validators.Optional()])

# regular views
@login_manager.user_loader
def load_user(id):
    try:
        user = db.session.query(User).filter(User.user_id == id).one()
        g.user = user
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

        if manager.check(user.password, password):
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

        hashed_password = manager.encode(password)
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

@app.route("/")
def main_index():
    session = db.session()
    maps = session.query(Map).all()

    return render_template('main_index.jinja', maps=maps)

def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
            filename.lower().rsplit('.', 1)[1] in allowed_extensions

@app.route("/submit", methods=['GET', 'POST'])
def submit_map():
    form = SubmitMapForm(request.form)
    if request.method == 'POST' and form.validate():
        map_name = form.name.data
        map_descr = form.description.data
        map_author = form.author.data
        map_version = form.version.data

        map_file = request.files[form.pk3.name]
        if map_file and allowed_file(map_file.filename,
                app.config['VALID_MAP_EXTENSIONS']):
            map_filename = secure_filename(map_file.filename)
            map_file.save(os.path.join(app.config['UPLOAD_FOLDER'], map_filename))

        map_screenshot = request.files[form.screenshot.name]
        if map_screenshot and allowed_file(map_screenshot.filename,
                app.config['VALID_SS_EXTENSIONS']):
            ss_filename = secure_filename(map_screenshot.filename)
            map_screenshot.save(os.path.join(app.config['UPLOAD_FOLDER'], ss_filename))

        m = Map(name=map_name, create_by=1)
        m.author = map_author
        m.descr = map_descr

        mf = File(file_type_cd="Xonotic Map", filename=map_filename,
                descr=map_descr, create_by=1)
        mf.md5sum = md5sum(os.path.join(app.config['UPLOAD_FOLDER'], mf.filename))

        ssf = File(file_type_cd="Screenshot", filename=ss_filename,
                descr="Primary screenshot", create_by=1)
        ssf.md5sum = md5sum(os.path.join(app.config['UPLOAD_FOLDER'], ssf.filename))

        db.session.add_all([m, mf, ssf])
        db.session.flush()

        mv = MapVersion(version=map_version, create_by=1)
        mv.map_id = m.map_id
        mv.file_id = mf.file_id
        db.session.add(mv)

        mss = MapScreenshot(name="Primary screenshot for {0}".format(map_name),
                create_by=1)
        mss.map_id = m.map_id
        mss.file_id = ssf.file_id
        db.session.add(mss)

        db.session.commit()
        return redirect(url_for('main_index'))

    else:
        return render_template('submit_map.jinja', form=form)

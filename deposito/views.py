import os
from cryptacular.bcrypt import BCRYPTPasswordManager
from deposito import *
from deposito.models import *
from deposito.util import md5sum
from flask import Flask, render_template, request, redirect, url_for
from flask import flash, g, session
from flask_login import login_required, login_user
from werkzeug import secure_filename


@login_manager.user_loader
def load_user(id):
    try:
        user = db.session.query(User).filter(User.user_id == id).one()
    except:
        user = None

    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    print "I'm in the login handler"
    # a login request
    if request.method == 'POST':
        username = request.form.get('username', None)
        password = request.form.get('password', None)

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
        return render_template('login.jinja', next=url_for('main_index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    print "I'm in the registration handler"
    # a registration request
    if request.method == 'POST':
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        password_confirm = request.form.get('password_confirm', None)

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
        user.active_ind = True
        db.session.add(user)
        db.session.commit()
        flash("Account {0} created successfully.".format(user.username))

        return redirect(url_for("main_index"))

    # not a POST, just showing the register form
    else:
        return render_template('register.jinja')

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
    if request.method == 'POST':
        map_name = request.form.get('map_name', None)
        map_descr = request.form.get('map_descr', None)
        map_author = request.form.get('map_author', None)
        map_version = request.form.get('map_version', None)
        map_filename = None
        ss_filename = None

        map_file = request.files['map_file']
        if map_file and allowed_file(map_file.filename,
                app.config['VALID_MAP_EXTENSIONS']):
            map_filename = secure_filename(map_file.filename)
            map_file.save(os.path.join(app.config['UPLOAD_FOLDER'], map_filename))

        map_screenshot = request.files['map_screenshot']
        if map_screenshot and allowed_file(map_screenshot.filename,
                app.config['VALID_SS_EXTENSIONS']):
            ss_filename = secure_filename(map_screenshot.filename)
            map_screenshot.save(os.path.join(app.config['UPLOAD_FOLDER'], ss_filename))

        # licenses are in all sorts of different checkboxes
        licenses = []
        for l in ('GPLv2', 'GPLv3', 'MIT', 'BSD', 'Apache', 'CC BY',
                'CC BY-SA', 'CC BY-ND', 'CC BY-NC', 'CC BY-NC-SA',
                'CC BY-NC-ND', 'Other'):
            val = request.form.get(l, None)
            if val is not None:
                licenses.append(val)

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
        return render_template('submit_map.jinja')

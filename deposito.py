import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug import secure_filename
from models import *
from util import md5sum

app = Flask(__name__)
app.config.from_object('settings')
app.config.from_envvar('DEPOSITO_SETTINGS')
db.init_app(app)

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

if __name__ == "__main__":
    app.run(debug=True)

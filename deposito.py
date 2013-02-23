import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug import secure_filename
from models import *

app = Flask(__name__)
app.config.from_object('settings')
app.config.from_envvar('DEPOSITO_SETTINGS')
db.init_app(app)

@app.route("/")
def main_index():
    session = db.session()
    maps = session.query(Map).all()

    return render_template('main_index.jinja', maps=maps)

def allowed_file(filename):
    return '.' in filename and \
            filename.lower().rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/submit", methods=['GET', 'POST'])
def submit_map():
    if request.method == 'POST':
        file = request.files['mapfile']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('main_index'))
    else:
        return render_template('submit_map.jinja')

if __name__ == "__main__":
    app.run(debug=True)

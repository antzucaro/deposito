from flask import Flask, render_template
from models import *

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///deposito.db'
db.init_app(app)

@app.route("/")
def main_index():
    session = db.session()
    maps = session.query(Map).all()

    return render_template('main_index.jinja', maps=maps)

if __name__ == "__main__":
    app.run(debug=True)

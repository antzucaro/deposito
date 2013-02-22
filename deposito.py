from flask import Flask
from models import *

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///deposito.db'
db.init_app(app)

@app.route("/")
def hello():
    return "Hello, deposito!"

if __name__ == "__main__":
    app.run()

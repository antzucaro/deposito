from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy

# Note: since we're not binding the app here, we have to call
# db.create_all(app=app) from the command line to create the tables
# and for more stuff (like a session), you'll need app.test_request_context()
db = SQLAlchemy()

class File(db.Model):
    __tablename__ = 'files'
    __table_args__ = {'sqlite_autoincrement':True}

    file_id      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filetype     = db.Column(db.String(100))
    filename     = db.Column(db.String(100))
    descr        = db.Column(db.String(300))
    size         = db.Column(db.Integer)
    md5sum       = db.Column(db.String(32))
    create_by    = db.Column(db.Integer)
    create_dt    = db.Column(db.DateTime)
    update_by    = db.Column(db.Integer)
    update_dt    = db.Column(db.DateTime)

    def __init__(self, filetype, filename, descr, create_by):
        self.filetype     = filetype
        self.filename     = filename
        self.descr        = descr
        self.update_by    = create_by
        self.create_dt    = datetime.utcnow()
        self.update_dt    = self.create_dt

    def __repr__(self):
        return '<File %s (%s)>' % (self.name, self.filetype)

class Map(db.Model):
    __tablename__ = 'maps'
    __table_args__ = {'sqlite_autoincrement':True}

    map_id       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name         = db.Column(db.String(100))
    approved     = db.Column(db.Boolean)
    downloadable = db.Column(db.Boolean)
    file_id      = db.Column(db.Integer)
    create_by    = db.Column(db.Integer)
    create_dt    = db.Column(db.DateTime)
    update_by    = db.Column(db.Integer)
    update_dt    = db.Column(db.DateTime)

    def __init__(self, name, create_by):
        self.name         = name
        self.approved     = False
        self.downloadable = False
        self.create_by    = create_by
        self.update_by    = create_by
        self.create_dt    = datetime.utcnow()
        self.update_dt    = self.create_dt

    def __repr__(self):
        return '<Map %s>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'sqlite_autoincrement':True}

    user_id     = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username    = db.Column(db.String(length=30), default='', unique=True)
    password    = db.Column(db.String(length=100), default='')
    active      = db.Column(db.Boolean, default=True)

    is_authenticated = False

    def is_authenticated(self):
        return self.is_authenticated

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return self.username != ""

    def get_id(self):
        return unicode(self.user_id)

    def __repr__(self):
        return '<User %s>' % self.username

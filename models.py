from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy

# Note: since we're not binding the app here, we have to call
# db.create_all(app=app) from the command line to create the tables
# and for more stuff (like a session), you'll need app.test_request_context()
db = SQLAlchemy()

class Map(db.Model):
    map_id       = db.Column(db.Integer, primary_key=True)
    name         = db.Column(db.String(100))
    approved     = db.Column(db.Boolean)
    downloadable = db.Column(db.Boolean)
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

class File(db.Model):
    file_id      = db.Column(db.Integer, primary_key=True)
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

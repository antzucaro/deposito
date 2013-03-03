from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy

# Note: since we're not binding the app here, we have to call
# db.create_all(app=app) from the command line to create the tables
# and for more stuff (like a session), you'll need app.test_request_context()
db = SQLAlchemy()

class FileType(db.Model):
    __tablename__ = 'cd_file_types'

    file_type_cd = db.Column(db.String(50), primary_key=True)
    descr        = db.Column(db.String(100))
    create_dt    = db.Column(db.DateTime, nullable=False)

    def __init__(self, file_type_cd=None, descr=None):
        self.file_type_cd = file_type_cd
        self.descr        = descr
        self.create_dt    = datetime.utcnow()

    def __repr__(self):
        return '%s' % self.file_type_cd

class License(db.Model):
    __tablename__ = 'cd_licenses'

    license_cd   = db.Column(db.String(50), primary_key=True)
    descr        = db.Column(db.String(300))
    create_dt    = db.Column(db.DateTime, nullable=False)

    def __init__(self, license_cd=None, descr=None):
        self.license_cd   = file_type_cd
        self.descr        = descr
        self.create_dt    = datetime.utcnow()

    def __repr__(self):
        return '%s' % self.license_cd

class ValidationCheck(db.Model):
    __tablename__ = 'cd_validations'

    validation_cd = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reason        = db.Column(db.String(100))
    descr         = db.Column(db.String(300))
    create_dt     = db.Column(db.DateTime, nullable=False)

    def __init__(self, validation_cd=None, descr=None):
        self.validation_cd = validation_cd
        self.descr         = descr
        self.create_dt     = datetime.utcnow()

    def __repr__(self):
        return '%s' % self.validation_cd

class File(db.Model):
    __tablename__ = 'files'

    file_id      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_type_cd = db.Column(db.String(50), db.ForeignKey("cd_file_types.file_type_cd"))
    filename     = db.Column(db.String(100))
    descr        = db.Column(db.String(300))
    size         = db.Column(db.Integer)
    md5sum       = db.Column(db.String(32))
    create_by    = db.Column(db.Integer, nullable=False)
    create_dt    = db.Column(db.DateTime, nullable=False)
    update_by    = db.Column(db.Integer, nullable=False)
    update_dt    = db.Column(db.DateTime, nullable=False)

    def __init__(self, file_type_cd=None, filename=None, descr=None, create_by=None):
        self.file_type_cd = file_type_cd
        self.filename     = filename
        self.descr        = descr
        self.create_by    = create_by
        self.update_by    = create_by
        self.create_dt    = datetime.utcnow()
        self.update_dt    = self.create_dt

    def __repr__(self):
        return '%s (%s)' % (self.filename, self.filetype)

class Map(db.Model):
    __tablename__ = 'maps'

    map_id       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name         = db.Column(db.String(100))
    author       = db.Column(db.String(50))
    descr        = db.Column(db.String(300))
    create_by    = db.Column(db.Integer, nullable=False)
    create_dt    = db.Column(db.DateTime, nullable=False)
    update_by    = db.Column(db.Integer, nullable=False)
    update_dt    = db.Column(db.DateTime, nullable=False)

    db.UniqueConstraint('name', name='map_uk01')

    def __init__(self, name=None, create_by=None):
        self.name         = name
        self.create_by    = create_by
        self.update_by    = create_by
        self.create_dt    = datetime.utcnow()
        self.update_dt    = self.create_dt

    def __repr__(self):
        return '%s' % self.name

class MapVersion(db.Model):
    __tablename__ = 'map_versions'

    map_ver_id   = db.Column(db.Integer, primary_key=True, autoincrement=True)
    map_id       = db.Column(db.Integer, db.ForeignKey("maps.map_id"))
    file_id      = db.Column(db.Integer, db.ForeignKey("files.file_id"))
    version      = db.Column(db.String(100))
    approved     = db.Column(db.Boolean)
    validated    = db.Column(db.Boolean)
    downloadable = db.Column(db.Boolean)
    create_by    = db.Column(db.Integer, nullable=False)
    create_dt    = db.Column(db.DateTime, nullable=False)
    update_by    = db.Column(db.Integer, nullable=False)
    update_dt    = db.Column(db.DateTime, nullable=False)

    def __init__(self, version=None, create_by=None):
        self.version      = version
        self.approved     = False
        self.validated    = False
        self.downloadable = False
        self.create_by    = create_by
        self.update_by    = create_by
        self.create_dt    = datetime.utcnow()
        self.update_dt    = self.create_dt

    def __repr__(self):
        return '<MapVersion(%d)>' % self.map_ver_id

class MapScreenshot(db.Model):
    __tablename__ = 'map_screenshots'

    mss_id       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    map_ver_id   = db.Column(db.Integer, db.ForeignKey("map_versions.map_ver_id"))
    file_id      = db.Column(db.Integer, db.ForeignKey("files.file_id"))
    name         = db.Column(db.String(100))
    width        = db.Column(db.Integer)
    height       = db.Column(db.Integer)
    create_by    = db.Column(db.Integer, nullable=False)
    create_dt    = db.Column(db.DateTime, nullable=False)
    update_by    = db.Column(db.Integer, nullable=False)
    update_dt    = db.Column(db.DateTime, nullable=False)

    def __init__(self, name, create_by):
        self.name         = name
        self.create_by    = create_by
        self.update_by    = create_by
        self.create_dt    = datetime.utcnow()
        self.update_dt    = self.create_dt

    def __repr__(self):
        return '<MapScreenshot(%d)>' % self.mss_id

class MapLicense(db.Model):
    __tablename__ = 'map_licenses'

    ml_id        = db.Column(db.Integer, primary_key=True, autoincrement=True)
    map_ver_id   = db.Column(db.Integer, db.ForeignKey("map_versions.map_ver_id"))
    license_cd   = db.Column(db.String(50), db.ForeignKey("cd_licenses.license_cd"))
    create_dt    = db.Column(db.DateTime, nullable=False)

    def __init__(self):
        self.create_dt    = datetime.utcnow()

    def __repr__(self):
        return '<MapLicense(%d)>' % self.ml_id

class MapValidation(db.Model):
    __tablename__ = 'map_validations'

    mv_id         = db.Column(db.Integer, primary_key=True, autoincrement=True)
    map_ver_id    = db.Column(db.Integer, db.ForeignKey("map_versions.map_ver_id"))
    validation_cd = db.Column(db.String(50), db.ForeignKey("cd_licenses.license_cd"))
    create_dt     = db.Column(db.DateTime, nullable=False)

    def __init__(self):
        self.create_dt    = datetime.utcnow()

    def __repr__(self):
        return '<MapValidation(%d)>' % self.mv_id

class MapTag(db.Model):
    __tablename__ = 'map_tags'

    tag_id        = db.Column(db.Integer, primary_key=True, autoincrement=True)
    map_ver_id    = db.Column(db.Integer, db.ForeignKey("map_versions.map_ver_id"))
    tag           = db.Column(db.String(50))
    create_dt     = db.Column(db.DateTime, nullable=False)

    def __init__(self):
        self.create_dt    = datetime.utcnow()

    def __repr__(self):
        return '<MapTag(%s)>' % self.tag

class User(db.Model):
    __tablename__ = 'users'

    user_id     = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username    = db.Column(db.String(length=30), default='', unique=True)
    password    = db.Column(db.String(length=100), default='')
    email       = db.Column(db.String(length=300), default='')
    about       = db.Column(db.String(length=300), default='')
    openid      = db.Column(db.String(length=300), default='')
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

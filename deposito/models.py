from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Note: since we're not binding the app here, we have to call
# db.create_all(app=app) from the command line to create the tables
# and for more stuff (like a session), you'll need app.test_request_context()
db = SQLAlchemy()


class Map(db.Model):
    __tablename__ = "map"

    map_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    author = db.Column(db.String(50))
    description = db.Column(db.String(300))
    create_by = db.Column(db.Integer, nullable=False)
    create_dt = db.Column(db.DateTime, nullable=False)
    update_by = db.Column(db.Integer, nullable=False)
    update_dt = db.Column(db.DateTime, nullable=False)

    db.UniqueConstraint("name", name="map_uk01")

    def __init__(self, name, author, description=None, create_by=None):
        self.name = name
        self.author = author
        self.description = description
        self.create_by = create_by
        self.update_by = create_by
        self.create_dt = datetime.utcnow()
        self.update_dt = self.create_dt

    def __repr__(self):
        return "<Map {0.name}>".format(self)


class MapVersion(db.Model):
    __tablename__ = "map_version"

    map_version_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    map_id = db.Column(db.Integer, db.ForeignKey("map.map_id"))
    version = db.Column(db.String(100))
    file = db.Column(db.String(500))
    size = db.Column(db.Integer)
    md5sum = db.Column(db.String(32))
    sha256sum = db.Column(db.String(64))
    primary = db.Column(db.Boolean)
    approved = db.Column(db.Boolean)
    validated = db.Column(db.Boolean)
    downloadable = db.Column(db.Boolean)
    create_by = db.Column(db.Integer, nullable=False)
    create_dt = db.Column(db.DateTime, nullable=False)
    update_by = db.Column(db.Integer, nullable=False)
    update_dt = db.Column(db.DateTime, nullable=False)

    def __init__(self, map_id, version, file, primary=False, create_by=None):
        self.map_id = map_id
        self.version = version
        self.file = file # TODO: calculate size, md5sum, and sha256sum
        self.primary = primary
        self.approved = False
        self.validated = False
        self.downloadable = False
        self.create_by = create_by
        self.update_by = create_by
        self.create_dt = datetime.utcnow()
        self.update_dt = self.create_dt

    def __repr__(self):
        return "<MapVersion {0.map_version_id>".format(self)


class MapScreenshot(db.Model):
    __tablename__ = "map_screenshot"

    map_screenshot_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    map_id = db.Column(db.Integer, db.ForeignKey("map.map_id"))
    name = db.Column(db.String(100))
    file = db.Column(db.String(500))
    size = db.Column(db.Integer)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    create_by = db.Column(db.Integer, nullable=False)
    create_dt = db.Column(db.DateTime, nullable=False)
    update_by = db.Column(db.Integer, nullable=False)
    update_dt = db.Column(db.DateTime, nullable=False)

    def __init__(self, map_id, name, file, create_by=None):
        self.map_id = map_id
        self.file = file
        self.name = name
        self.primary = False
        self.create_by = create_by
        self.update_by = create_by
        self.create_dt = datetime.utcnow()
        self.update_dt = self.create_dt

    def __repr__(self):
        return "<MapScreenshot {0.file}>".format(self)


class License(db.Model):
    __tablename__ = "cd_license"

    license_cd = db.Column(db.String(50), primary_key=True)
    descr = db.Column(db.String(300))
    create_dt = db.Column(db.DateTime, nullable=False)

    def __init__(self, license_cd=None, descr=None):
        self.license_cd = license_cd
        self.descr = descr
        self.create_dt = datetime.utcnow()

    def __repr__(self):
        return "<License {0.license_cd}>".format(self)


class MapLicense(db.Model):
    __tablename__ = "map_license"

    map_license_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    map_version_id = db.Column(db.Integer, db.ForeignKey("map_version.map_version_id"))
    license_cd = db.Column(db.String(50), db.ForeignKey("cd_license.license_cd"))
    create_dt = db.Column(db.DateTime, nullable=False)

    def __init__(self, map_version_id, license_cd):
        self.map_version_id = map_version_id
        self.license_cd = license_cd
        self.create_dt = datetime.utcnow()

    def __repr__(self):
        return "<MapLicense {0.map_license_id}>".format(self)


class User(db.Model):
    __tablename__ = "user"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(length=30), default='', unique=True)
    password = db.Column(db.String(length=100), default='')
    email = db.Column(db.String(length=300), default='')
    about = db.Column(db.String(length=300), default='')
    openid = db.Column(db.String(length=300), default='')
    active = db.Column(db.Boolean, default=True)

    authenticated = False

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return self.username != ""

    def get_id(self):
        return unicode(self.user_id)

    def __repr__(self):
        return "<User {0.username}>".format(self)

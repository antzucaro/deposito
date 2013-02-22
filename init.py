from deposito import *

# setup some test data
def setup_test_data():
    with app.test_request_context():
        adminuser = User()
        adminuser.username = "admin"
        adminuser.password = "admin"
        db.session.add(adminuser)
        db.session.flush()

        dance_f = File(filetype="map", filename="dance.pk3",
                descr="Your favorite way to dance.", create_by=adminuser.user_id)
        db.session.add(dance_f)
        db.session.flush()

        dance = Map(name="dance", create_by=adminuser.user_id)
        dance.file_id = dance_f.file_id
        db.session.add(dance)

        dance_ss_f = File(filetype="image", filename="dance.jpg",
                descr="Image caption", create_by=adminuser.user_id)
        db.session.add(dance_ss_f)
        db.session.flush()

        dance_ss = Screenshot(name="dance primary screenshot", create_by=adminuser.user_id)
        dance_ss.width = 50
        dance_ss.height = 50
        dance_ss.file_id = dance_ss_f.file_id
        db.session.add(dance_ss)

        db.session.commit()

# if called from the command line, we set up the database tables only
if __name__ == "__main__":
    db.create_all(app=app)

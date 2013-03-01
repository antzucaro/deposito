from deposito import *

# if called from the command line, we set up the database tables only
if __name__ == "__main__":
    db.create_all(app=app)

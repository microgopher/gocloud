#!/usr/bin/env python
from flask.script import Manager
from models import db, RoleModel
from app import create_app


manager = Manager(create_app)


@manager.command
def createdb(testdata=True):
    """Initializes the database """
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        if testdata:
            role = RoleModel(name='admin')
            db.session.add(role)
            db.session.commit()

if __name__ == '__main__':
    manager.run()

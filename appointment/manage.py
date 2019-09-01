#!/usr/bin/env python
from flask.script import Manager
from models import db, AppointmentModel
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
            appointment = AppointmentModel(name='test')
            db.session.add(appointment)
            db.session.commit()

if __name__ == '__main__':
    manager.run()

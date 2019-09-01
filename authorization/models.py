from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Base(db.Model):
    """ Base model from which other models will inherit from """
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    hex_id = db.Column(db.String(20), unique=True, nullable=False, default=lambda:secrets.token_hex(20))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    active = db.Column(db.Boolean, default=True)
    #created_by = db.Column(db.String(20), nullable=False) # current user's hex_id
    #updated_by = db.Column(db.String(20)) #current user's hex_id

    def save(self):
        """ Save the object instance of the model """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """ Deletes the object instance of the model """
        db.session.delete(self)
        db.session.commit()

    def to_json(self):
        """ Serializes objects to json """
        json_dict = dict()
        result_list = []
        for property in class_mapper(self.__class__).iterate_properties:
            json_dict[property.key] = getattr(self, property.key)
        return json_dict


permission_activities = db.Table('permission_activities',
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'), primary_key=True),
    db.Column('activity_id', db.Integer, db.ForeignKey('activities.id'), primary_key=True)
)

role_permission = db.Table('role_permission',
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'), primary_key=True)
)

class RoleModel(Base):
    __tablename__ = 'roles'
    name = db.Column(db.String, nullable=False)
    permissions = db.relationship('PermissionModel', secondary=role_permission, lazy='subquery', back_populates='roles')

class PermissionModel(db.Model):
    __tablename__ = 'permissions'
   
    name = db.Column(db.String, nullable=False)
    role_id = db.Column(db.Integer)
    activities = db.relationship('ActivityModel', secondary=permission_activities, lazy='subquery', backref='permissions')
    

class ActivityModel(db.Model):
    __tablename__ = 'activities'

    url = db.Column(db.String, nullable = False)
    method = db.Column(db.String(10), nullable = False)

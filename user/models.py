
from passlib.hash import pbkdf2_sha256 as sha256
import secrets


from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import orm
import hashlib

db = SQLAlchemy()
class_mapper = orm.class_mapper


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




class UserModel(Base):
    __tablename__ = 'users'

    username = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String, nullable = False)
    name = db.Column(db.String(256), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    mobile = db.Column(db.String(120), nullable=True)
    roles = db.Column(db.String)
    
    
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first()

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)
    
    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

class RevokedTokenModel(Base):
    __tablename__ = 'revoked_tokens'
    jti = db.Column(db.String(120))
    
    
    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti = jti).first()
        return bool(query)

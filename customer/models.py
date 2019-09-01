import math
from flask_sqlalchemy import SQLAlchemy
import secrets
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

    def page_query(query, formatter=None, page_size=10, page=False):
        num_pages = 1
        total_results = query.count()
        if page_size is not None:
            num_pages = math.ceil(total_results / page_size)

            if page >= num_pages:
                return 
            
            offset = page * page_size
            query = query.offset(offset).limit(page_size)

        num_returned = query.count()
        results = query.all()

        if formatter is not None:
            results = formatter(results)
        
        return {
            'page': page,
            'total_pages': num_pages,
            'total_results': total_results,
            'num_returned': num_returned,
            'results': results
        }


class CustomerModel(Base):
    __tablename__ = 'Customers'

    name = db.Column(db.String(120), nullable = False)    
    address = db.Column(db.String(256), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    mobile = db.Column(db.String(120), nullable=True)
    user_id = db.Column(db.String(20), nullable=False)
    
    
    
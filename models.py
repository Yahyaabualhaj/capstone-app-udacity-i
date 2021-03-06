import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Student
a persistent student entity, extends the base SQLAlchemy Model
'''
class Student(db.Model):
    # Autoincrementing, unique primary key
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)

    first_name = Column(String(80), nullable=False)
    last_name = Column(String(80), nullable=False)
    age = Column(Integer, nullable=False)
  
    '''
    json_data()
        json form representation of the Student model
    '''
    def short_data(self):
        return  {
            'id': self.id,
            'first_name': self.first_name,       
        }
        
    def detial_data(self):
        return  {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age': self.age,
        }


    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            student = Student(first_name=req_first_name, last_name=req_name, age=req_age)
            student.insert()
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a model into a database
        the model must exist in the database
        EXAMPLE
            student.delete()
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a  model into a database
        the model must exist in the database
        EXAMPLE
            student = Student.query.filter(Student.id == id).one_or_none()
            
            student.first_name = 'Yahya'
            student.last_name = 'Abu Alhaj'
            student.age = '40'
            student.update()
    '''
    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.first_name)
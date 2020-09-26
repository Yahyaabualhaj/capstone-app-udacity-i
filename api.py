import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from database.models import db_drop_and_create_all, setup_db, Student
from auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

## ROUTES
'''
    GET /students
     
    returns status code 200 and json {"success": True, "students": students} where students is the list of students
        or appropriate status code indicating reason for failure
'''

@app.route('/students', methods=['GET'])
def retrieve_students():
    all_students = Student.query.all()  
    data = {'success': True,'students': [student.short_data() for student in all_students]}
    return jsonify(data)

'''
    GET /students
     
    returns status code 200 and json {"success": True, "student": student} where student is the detial information of specific student
        or appropriate status code indicating reason for failure
'''

 
# also add payload to arg.
@app.route('/students/<int:id>', methods=['GET'])
@requires_auth('get:students-detail')
def get_student_detail(payload,id):
    student = Student.query.filter(Student.id==id).one_or_none()
    
    data = {'success': True,'students': student.detial_data()}
    return jsonify(data)


'''
    POST /Students
        it should create a new row in the Students table
        it should require the 'post:Students' permission
        it should contain the Student.long() data representation
    returns status code 200 and json {"success": True, "Students": Student} where Student an array containing only the newly created Student
        or appropriate status code indicating reason for failure
'''
# @requires_auth('post:Students')
@app.route('/students', methods=['POST'])
@requires_auth('post:students')
def create_student(payload):
    
    body = request.get_json()
  
    first_name = body.get('first_name',None)
    last_name = body.get('last_name',None)
    age = body.get('age',None)
    print('first name : ',body)
    
    try:
        new_student = Student(
            first_name=first_name, 
            last_name=last_name,
            age=age,
            )
        
        new_student.insert()
    except:
        abort(422)
    
    
    data = {"success": True, "students": new_student.detial_data()}
    return jsonify(data)

'''
    PATCH /Students/<id>
        where <id> is the existing model id
 
    returns status code 200 and json {"success": True, "studnents": stundent} where student an array containing only the updated student
        or appropriate status code indicating reason for failure
'''
@app.route('/students/<int:id>', methods=['PATCH'])
@requires_auth('patch:students')
def update_Student(id):
    
    body = request.get_json()
  
    first_name = body.get('first_name',None)
    last_name = body.get('last_name',None)
    age = body.get('age',None)
    
    student = Student.query.filter(Student.id == id).one_or_none()
    if student is None:
        abort(404)
    try:    
        student.first_name = first_name
        student.last_name = last_name
        student.age = age
        student.update()
    except:
        abort(422)
        
    data = {"success": True, "students": student.detial_data()}
    return jsonify(data)

'''
    DELETE /Students/<id>
        where <id> is the existing model id
       
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/students/<int:id>',methods=['DELETE'])
@requires_auth('delete:students')
def delete_student(id):
    get_student = Student.query.filter(Student.id == id).one_or_none()
    if get_student is None:
        abort(404)
        
    try:    
        get_student.delete()
        data = {"success": True, "delete": id}
    except:
        abort(422)
        
    return jsonify(data)



# Error Handling

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422


     
@app.errorhandler(404)
def not_found(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404


@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
                    "success": False, 
                    "error": error.status_code,
                    "message": error.error['description']
                    }), error.status_code


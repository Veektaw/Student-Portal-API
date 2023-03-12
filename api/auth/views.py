from flask import request
import random, string
from flask_restx import Namespace, Resource, fields
from ..models.students import Student
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

auth_namespace = Namespace('auth', description='name space for authentication')




signup_expect_model = auth_namespace.model(
    'Student',{
        'first_name': fields.String(description='First name of the student', required=True,),
        'last_name': fields.String(description='Last name of the student', required=True),
        'email': fields.String(description="Email of student", required=True),
        'student_password': fields.String(description='Password of student', required=True)                          
    }
)


signup_model = auth_namespace.model(
    'StudentSign',{
        'id': fields.Integer(description='An order ID'),
        'first_name': fields.String(description='First name of the student', required=True,),
        'last_name': fields.String(description='Last name of the student', required=True),
        'email': fields.String(description="Email of student", required=True),
        'student_password': fields.String(description='Password of student', required=True)                          
    }
)




student_login = auth_namespace.model(
    'StudentLogin',{
        'email': fields.String(description="Email of student", required=True),
        'student_password': fields.String(description='Password of student', required=True)                          
    }
)
   


@auth_namespace.route('/signup')
class SignUp(Resource):
   
   @auth_namespace.expect(signup_expect_model)
   @auth_namespace.marshal_with(signup_model)
   @auth_namespace.doc(description="Signup student")
   def post(self):
     
      data = request.get_json()

      new_student = Student(
         first_name = data.get('first_name'),
         last_name = data.get('last_name'),
         email = data.get('email'),
         student_password = generate_password_hash(data.get('student_password'))
      )

      new_student.save()

      return new_student, HTTPStatus.CREATED
   


@auth_namespace.route('/login')
class Login(Resource):
   
   @auth_namespace.expect(student_login)
   @auth_namespace.doc(description="Login admin")
   def post(self):
     
      data = request.get_json()

      email = data.get("email")
      student_password = data.get("student_password")

      student = Student.query.filter_by(email=email).first()

      if (student is not None) and check_password_hash(student.student_password, student_password):
         access_token = create_access_token(identity=student.email)
         refresh_token = create_refresh_token(identity=student.email)

         response = {
            'access_token': access_token,
            'refresh_token': refresh_token
         }

         return response, HTTPStatus.CREATED
     
@auth_namespace.route('/refresh')
class Refresh(Resource):

   @auth_namespace.doc(description="Refresh access token of user login")
   @jwt_required(refresh=True)
   def post(self):
      username = get_jwt_identity()

      access_token = create_access_token(identity=username)

      return {"access_token": access_token}, HTTPStatus.OK


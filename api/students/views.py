from flask import request
import random, string
from flask_restx import Namespace, Resource, fields
from ..models.students import Student
from ..models.grades import Grade
from ..models.registration import Registration
from http import HTTPStatus
from werkzeug.security import generate_password_hash, check_password_hash
from ..utility import db
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity


student_namespace = Namespace('students', description='Namespace for students')

student_model = student_namespace.model(
    'Student',{
        'id': fields.Integer(description='An order ID'),
        'first_name': fields.String(description='First name of the student', required=True,),
        'last_name': fields.String(description='Last name of the student', required=True),
        'email': fields.String(description="Email of student", required=True),
        'student_password': fields.String(description='Password of student', required=True)                          
    }
)


student_model_GPA = student_namespace.model(
    'Student',{
        'id': fields.Integer(description='An order ID'),
        'first_name': fields.String(description='First name of the student', required=True,),
        'last_name': fields.String(description='Last name of the student', required=True),
        'email': fields.String(description="Email of student", required=True),
        'student_gpa': fields.Float(description='GPA of the student'),
        'student_password': fields.String(description='Password of student', required=True)                          
    }
)




grade_model = student_namespace.model(
    'StudentGrades',{
        'last_name': fields.String(description='Last name of the student', required=True,),
        'student_email': fields.String(description='name of student', required=True,),
        'course_unit': fields.Integer(description="Unit of the course", required=True),
        'course_name': fields.String(description="Name of the course", required=True),
        'student_grade' : fields.Integer(description="Grade of the student", required=True),
        'student_id': fields.Integer(description='ID of student')         
    }
)


student_update_model = student_namespace.model(
    'StudentUpdate',{
        'id': fields.String(description='ID of the student'),
        'first_name': fields.String(description='name of student', required=True,),
        'last_name': fields.String(description='name of student', required=True,),
        'email': fields.String(description="Email of student", required=True)                          
    }
)



student_course_model = student_namespace.model(
    'StudentCourseModel', {
        'last_name': fields.String(description='Last name of student', required=True,),
        'course_name': fields.String(description='Name of Course', required=True,),
        'student_email': fields.String(description="Email of student", required=True),
        'student_id': fields.Integer(description='ID of student', required=True,),
        'course_id': fields.Integer(description="ID of course", required=True)
    }
)




@student_namespace.route('/students')
class StudentGetCreate(Resource):

    @student_namespace.marshal_list_with(student_model)
    @student_namespace.doc(description="Get all students")
    @jwt_required()
    def get(self):
        
        """
            Get all students
        """
        try:
            students = Student.query.all()
            
        except:
            return {'Message':"Could not get all students"}
        
        return students, HTTPStatus.OK




@student_namespace.route("/student/<int:student_id>")
class GetUpdateDelete(Resource):

    @student_namespace.marshal_with(student_model_GPA)
    @student_namespace.doc(description="Get a student by ID",
                           params={'student_id' :'An ID of the student'})
    @jwt_required()
    def get(self, student_id):
        
        """
            Get a particular student, this includes the GPA of said student
        """
        try:
            
            email = get_jwt_identity()

            current_user = Student.query.filter_by(email=email).first()
            
            student = Student.get_by_id(student_id)
            
            
            if current_user == current_user:
        
                grades = Grade.query.filter_by(student_id=student_id).all()

                total_course_units = sum([grade.course_unit for grade in grades])
                total_grade_points = sum([grade.student_grade * grade.course_unit for grade in grades])

                student_gpa = total_grade_points / total_course_units if total_course_units > 0 else 0

                for grade in grades:
                    grade = Student.query.filter_by(email=email).first()
                    grade.student_gpa = student_gpa
                    db.session.add(grade)
                    db.session.commit()
            else:
                return {'Message':"You do not have access"}
                    
        
            
        except:
            return {'Message':"Could not get this student"}
        
        return student, HTTPStatus.OK




    @student_namespace.expect(student_update_model)
    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(description="Update a student",
                           params={'student_id' :'An ID of the student'})
    @jwt_required()
    def put(self, student_id):
        """
            Admin updates a student
        
        """
        
        
        email = get_jwt_identity()

        current_user = Student.query.filter_by(email=email).first()
        
        
        if current_user.id != 1:
            return {'Message': 'You do not have access'}
        
        else:
        
            student_to_update = Student.get_by_id(student_id)

            data = student_namespace.payload

            student_to_update.first_name = data['first_name']
            student_to_update.last_name = data['last_name']
            student_to_update.email = data['email']

            student_to_update.update()

            return student_to_update, HTTPStatus.OK



    @student_namespace.doc(description="Delete a student",
                           params={'student_id' :'An ID of the student'})
    @jwt_required()
    def delete(self, student_id):
        """
            Admin deletes a student
        
        """
        
        email = get_jwt_identity()

        current_user = Student.query.filter_by(email=email).first()
        
        
        if current_user.id != 1:
            return {'Message': 'You do not have access'}
        
          
        else:
            student_to_delete = Student.get_by_id(student_id)
        
            student_to_delete.delete()

            return {"message": "Student deleted"}, HTTPStatus.OK
    
   


@student_namespace.route("/student/<int:student_id>/grades")
class GetStudentGrades(Resource):

    @student_namespace.marshal_with(grade_model)
    @student_namespace.doc(description="Get a specific student's specific grade",
                         params={'student_id': 'student ID'})
    @jwt_required()
    def get(self, student_id):
        
        """ 
            Grades of a specific student
        
        """
        email = get_jwt_identity()

        current_user = Student.query.filter_by(email=email).first()
        
        
        if current_user == current_user:
            student_courses = Grade.query.filter_by(student_id=student_id).all()
        
        else:
            return {'Message':"Could not get this student's grades"}
        
        return student_courses, HTTPStatus.OK
    
    
@student_namespace.route("/student/<int:student_id>/courses")
class GetStudentCourses(Resource):

    @student_namespace.marshal_list_with(student_course_model)
    @student_namespace.doc(description="Get a specific student's courses",
                         params={'student_id': 'student ID'})
    @jwt_required()
    def get(self, student_id):
        
        """ 
            Courses of a specific student
        
        """
              
        #student = Grade.get_by_id(student_id)
        try:
            student_courses = Registration.query.filter_by(student_id=student_id).all()
        
        except:
            return {'Message':"Could not get this student's courses"}
        
        return student_courses, HTTPStatus.OK
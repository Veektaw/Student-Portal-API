from flask import request
from flask_restx import Namespace, Resource, fields
from ..models.courses import Course
from ..models.students import Student
from ..models.registration import Registration
from ..models.grades import Grade
from http import HTTPStatus
from werkzeug.security import generate_password_hash, check_password_hash
from ..utility import db
from flask_jwt_extended import jwt_required, get_jwt_identity


course_namespace = Namespace('courses', description='Namespace for courses')

admin_course_reg_model = course_namespace.model(
    'CourseExpect', {
        'course_name': fields.String(description='Course name', required=True),
        'course_teacher': fields.String(description='Course teacher', required=True),
        'course_unit': fields.Integer(description='Course unit', required=True),
    }
)


course_model = course_namespace.model(
    'CourseModel', {
        'id' : fields.Integer(description='Database id of a course'),
        'course_name': fields.String(description='Course name'),
        'course_teacher': fields.String(description='Course teacher'),
        'course_unit': fields.Integer(description='Course unit')
    }
)



student_course_model = course_namespace.model(
    'Student_Course',{
        'last_name': fields.String(description='First name of course', required=True),
        'course_name': fields.String(description='Name of the course', required=True),
        'student_email': fields.String(description='First name of course', required=True),
        'student_id': fields.Integer(description="Last name of student", required=True),
        'course_id': fields.Integer(description="First name of student", required=True)                         
    }
)

grade_model = course_namespace.model(
    'StudentGradesEntry',{
        'last_name': fields.String(description='Last name of the student', required=True,),
        'student_email': fields.String(description='name of student', required=True,),
        'course_name': fields.String(description='Name of the course', required=True),
        'course_unit': fields.Integer(description="Unit of the course", required=True),
        'student_grade' : fields.Integer(description="Grade of the student", required=True),
        'student_id': fields.Integer(description="Student ID", required=True),
        'course_id': fields.Integer(description="Course ID", required=True),                     
    }
)


@course_namespace.route('/course/course_reg')
class AdminCourseReg(Resource):
   
   @course_namespace.expect(admin_course_reg_model)
   @course_namespace.marshal_with(course_model)
   @course_namespace.doc(description="Admin registers course")
   @jwt_required()
   def post(self):
        

        """
            Admin registers a course to the databse
        """
     
        email = get_jwt_identity()

        current_user = Student.query.filter_by(email=email).first()
        
        
        if current_user.id != 1:
            return {'Message': 'You do not have access'}
        
        
        else:

            data = course_namespace.payload

            new_course = Course(
                course_name = data.get('course_name'),
                course_unit = data.get('course_unit'),
                course_teacher = data.get('course_teacher'),
            )

            new_course.student = current_user
    
            new_course.save()

            return new_course, HTTPStatus.CREATED
   

@course_namespace.route('/course')
class GetAllCourses(Resource):

    @course_namespace.marshal_list_with(course_model)
    @course_namespace.doc(description="Get all courses")
    @jwt_required()
    def get(self):

        """
            Get all courses
        """
        try:
            courses = Course.query.all()
            
        except:
            return {'Message':"Could not get all students"}

        return courses, HTTPStatus.OK
    

    
@course_namespace.route("/course/<int:course_id>")
class GetCourse(Resource):

    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(description="Get course by ID", 
                          params={'course_id' :'An ID of the course'})
    @jwt_required()
    def get(self, course_id):


        """
            Get a course by ID
        """
        try:
            course = Course.get_by_id(course_id)
            
        except:
            return {'Message':"Could not get all student"}
        
        return course, HTTPStatus.OK



@course_namespace.route("/course/<int:course_id>/students")
class GetAllCourseStudents(Resource):

    @course_namespace.marshal_with(student_course_model)
    @course_namespace.doc(description="Get all students by a specific course",
                         params={'course_id' :'A ccourse ID to get all students'})
    @jwt_required()
    def get(self, course_id):
        """
            Get all students of a specific course
        """
        
        try:
            course = Registration.query.filter_by(course_id=course_id).all()
            
        except:
            return {'Message':"Could not get students"}

        # Database relationship reference
        #students = course.student

        return course, HTTPStatus.OK
    


@course_namespace.route("/course/<int:course_id>/students/grades")
class GetAllStudentsGrades(Resource):

    @course_namespace.marshal_with(grade_model)
    @course_namespace.doc(description="Get grades of all students of a specific course",
                         params={'course_id' :'A ccourse ID to get all students'})
    @jwt_required()
    def get(self, course_id):
        """
            Get grades of all students of a specific course
        """
        #course_id = Registration.get_by_id(course_id)
        
        
        try:
            student_grades = Grade.query.filter_by(course_id=course_id).all()
            
        
        except:
            return {'Message':"Could not get student grades"}
        
        

        # Database relationship reference
        #students = course.student

        return student_grades, HTTPStatus.OK


    
    
    
    

@course_namespace.route('/course/student/student_reg')
class StudentCourseReg(Resource):
   
   @course_namespace.expect(student_course_model)
   @course_namespace.marshal_with(student_course_model)
   @course_namespace.doc(description="Student course registration")
   @jwt_required()
   def post(self):
        """
            Student registers for a course
        """


        email = get_jwt_identity()

        current_user = Student.query.filter_by(email=email).first()
        
        data = course_namespace.payload

        student_id = data.get('student_id')
        
        student = Student.query.filter_by(id=student_id).first()
        
        if not student:
            return {'message': 'Invalid student ID'}, HTTPStatus.BAD_REQUEST


        new_course_reg = Registration(
            last_name = data.get('last_name'),
            course_name = data.get('course_name'),
            student_email = data.get('student_email'),
            student_id = data.get('student_id'),
            course_id = data.get('course_id')
        )
            
            
        new_course_reg.student = current_user
    
        new_course_reg.save()

        return new_course_reg, HTTPStatus.CREATED
        
        
@course_namespace.route('/course/grade_entry')
class AdminGradeEntry(Resource):
   
   @course_namespace.expect(grade_model)
   @course_namespace.marshal_with(grade_model)
   @course_namespace.doc(description="Student course registration")
   @jwt_required()
   def post(self):
       
       
       
        """
            Admin enters student grades
        """
     
        email = get_jwt_identity()

        current_user = Student.query.filter_by(email=email).first()
        
        if current_user.id != 1:
            return {'Message': 'You do not have access'}
        
        
        
        else:
            data = course_namespace.payload

            grade_entry = Grade(
                last_name = data.get('last_name'),
                student_email = data.get('student_email'),
                course_name = data.get('course_name'),
                student_grade = data.get('student_grade'),
                course_unit = data.get('course_unit'),
                student_id = data.get('student_id'),
                course_id = data.get('course_id')
            )

            grade_entry.student = current_user
    
            grade_entry.save()

            return grade_entry, HTTPStatus.CREATED
    
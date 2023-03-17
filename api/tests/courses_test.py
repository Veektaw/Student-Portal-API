import unittest
from unittest.mock import patch, MagicMock
from .. import create_app
from ..config.config import config_dict
from ..utility import db
from werkzeug.security import generate_password_hash
from ..models.courses import Course
from ..models.registration import Registration
from ..models.grades import Grade
from ..models.students import Student
from flask_jwt_extended import create_access_token

class CourseTestCase(unittest.TestCase):
    
    def setUp(self):

        self.app = create_app(config=config_dict['test'])

        self.appctx = self.app.app_context()

        self.appctx.push()

        self.client = self.app.test_client()

        db.create_all()



    def tearDown(self):

        db.drop_all()

        self.appctx.pop()

        self.app = None
 
        self.client = None
        
        
    
    def test_all_courses(self):

        token = create_access_token(identity='testuser')

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = self.client.get('/course/course', headers=headers)

        assert response.status_code == 200

        assert response.json == []
        
        
        
    def test_get_course_byid(self):

        student = Student.query.filter_by(email='testuser@gmail.com').first()

        token = create_access_token(identity=student)

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = self.client.get('/course/course/1', headers=headers)

        assert response.status_code == 200
        
        
    # Admin registers a course to the database
    def test_admin_registers_course(self):

        student = Student(
            first_name='Test',
            last_name='Tester',
            email='testuser@gmail.com',
            student_password='password'
        )
        student.save()
        
        token = create_access_token(identity=student.email)

        self.return_value = student.email

        data = {
            'course_name': 'Test Course',
            'course_teacher': 'Mr Tester',
            'course_unit': 3
        }
        response = self.client.post('/course/course/course_reg', json=data, headers={'Authorization': f'Bearer {token}'})

        assert response.status_code == 201
        
        
    # Admin enters students grades to the database
    def test_admin_enters_grades(self):

        student = Student(
            first_name='Test',
            last_name='Tester',
            email='testuser@gmail.com',
            student_password='password'
        )
        student.save()
        
        token = create_access_token(identity=student.email)

        self.return_value = student.email

        data = {
            'last_name': 'Tester',
            'student_email': 'testuser@gmail.com',
            'course_name': 'Test Course',
            'student_grade': 70,
            'course_unit': 3,
            'student_id': student.id,
            'course_id': 1
        }
        response = self.client.post('/course/course/grade_entry', json=data, headers={'Authorization': f'Bearer {token}'})

        assert response.status_code == 201
     
     
        
    # Student registers for a course
    def test_student_registers_course(self):
        student = Student(
            first_name='Test',
            last_name='Tester',
            email='testuser@gmail.com',
            student_password='password'
        )
        student.save()
        
        token = create_access_token(identity=student.email)

        self.return_value = student.email

        registration_data = {
            'last_name': 'Tester',
            'course_name': 'Test Course',
            'student_email': 'testuser@gmail.com',
            'student_id': student.id,
            'course_id': 1
        }
        response = self.client.post('/course/course/student/student_reg', json=registration_data, headers={'Authorization': f'Bearer {token}'})

        assert response.status_code == 201
        
        
        
    # Get grades of students in a course
    def test_get_course_grades(self):
        
        student = Student.query.filter_by(email='testuser@gmail.com').first()

        token = create_access_token(identity=student)

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = self.client.get('/course/course/1/students/grades', headers=headers)

        assert response.status_code == 200
        
        
        
    # Get students of a specific course
    def test_get_course_students(self):
        
        student = Student.query.filter_by(email='testuser@gmail.com').first()

        token = create_access_token(identity=student)

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = self.client.get('/course/course/1/students', headers=headers)

        assert response.status_code == 200
    
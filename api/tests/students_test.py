import unittest
from .. import create_app
from ..config.config import config_dict
from ..utility import db
from http import HTTPStatus
from werkzeug.security import generate_password_hash
from ..models.students import Student
from flask_jwt_extended import create_access_token

class StudentTestCase(unittest.TestCase):
    
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

    def test_get_all_students(self):

        student = Student.query.filter_by(email='testuser@gmail.com').first()

        token = create_access_token(identity=student)

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = self.client.get('/student/students', headers=headers)

        assert response.status_code == 200

        assert response.json == []
        
        
        # Get student by ID
    def test_get_student_byid(self):
        
        student = Student.query.filter_by(email='testuser@gmail.com').first()

        token = create_access_token(identity=student)

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = self.client.get('/student/student/1', headers=headers)

        assert response.status_code == 200
        
        
    # Get a student's grades
    def test_get_student_grades(self):
        
        student = Student.query.filter_by(email='testuser@gmail.com').first()

        token = create_access_token(identity=student)

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = self.client.get('/student/student/1/grades', headers=headers)

        assert response.status_code == 200
        
        
    # Get a student's courses
    def test_get_student_courses(self):
        
        student = Student.query.filter_by(email='testuser@gmail.com').first()

        token = create_access_token(identity=student)

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = self.client.get('/student/student/1/courses', headers=headers)

        assert response.status_code == 200
        
        
        
    # Admin deletes a student
    def test_admin_deletes_student(self):

        student = Student(
            first_name='Test',
            last_name='Tester',
            email='testuser@gmail.com',
            student_password='password'
        )
        student.save()
        
        token = create_access_token(identity=student.email)

        self.return_value = student.email
        
        response = self.client.delete('/student/student/1', headers={'Authorization': f'Bearer {token}'})

        assert response.status_code == 200
        
    
    # Admin updates a student
    def test_admin_updates_student(self):

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
            'first_name': 'Testers',
            'last_name': 'Tests',
            'email': 'testuser@gmail.com'
        }
        
        response = self.client.put('/student/student/1',json=data, headers={'Authorization': f'Bearer {token}'})

        assert response.status_code == 200
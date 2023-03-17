import unittest
from unittest.mock import patch, MagicMock
from .. import create_app
from ..config.config import config_dict
from ..utility import db
from werkzeug.security import generate_password_hash
from ..models.courses import Course
from ..models.grades import Grade
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
        
        

    def test_courses_routes(self):

        token = create_access_token(identity='testuser@gmail.com')

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = self.client.get('/course/course', headers=headers)

        assert response.status_code == 200

        assert response.json == []



        data = {
            "size": "SMALL",
            "quantity": 1,
            "flavour": "Pepperoni"
        }

        token = create_access_token(identity='testuser')

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = self.client.post('/course/student/student_reg', json=data, headers=headers)

        assert response.status_code == 201

        orders = Course.query.all()

        assert len(orders) == 1
        assert response.status_code == 404
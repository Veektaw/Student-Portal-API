import unittest
from .. import create_app
from ..config.config import config_dict
from ..utility import db
from werkzeug.security import generate_password_hash
from ..models.students import Student
from flask_jwt_extended import create_access_token

class OrderTestCase(unittest.TestCase):
    
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

    def test_all_student_routes(self):

        token = create_access_token(identity='testuser')

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = self.client.get('/student/students', headers=headers)

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

        response = self.client.post('/orders/orders', json=data, headers=headers)

        assert response.status_code == 201

        students = Student.query.all()

        assert len(students) == 1
        assert response.status_code == 404
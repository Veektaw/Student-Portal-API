from flask import Flask, jsonify
from functools import wraps
from flask_restx import Api
from .courses.views import course_namespace
from .auth.views import auth_namespace
from .students.views import student_namespace
from .config.config import config_dict
from .utility import db
from .models.courses import Course
from .models.students import Student
from .models.grades import Grade
from .models.registration import Registration
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt, create_access_token
from werkzeug.exceptions import NotFound, NotAcceptable, MethodNotAllowed

def create_app(config=config_dict['test']):
    app = Flask(__name__)


    app.config.from_object(config)

    db.init_app(app)

    jwt = JWTManager(app)

    migrate = Migrate(app, db)

    authorizations = {
        'Bearer Auth':{
           "type": "apiKey",
           "in": "Header",
           "name": "Authorization",
           "description": "Add a JWT token to the header with ** Bearer <JWT Token>" 
        }
    }

    api = Api(app, title='Student portal API',
              description='A student portal API',
              version = 1.0,
              authorizations=authorizations,
              security='Bearer Auth')

    api.add_namespace(course_namespace, path='/course')
    api.add_namespace(student_namespace, path='/student')
    api.add_namespace(auth_namespace, path='/auth')

    @api.errorhandler(NotFound)
    def not_found(error):
        return {"error": "Not found"}, 404
    
    @api.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return {"error": "Method not allowed"}, 404

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'student': Student,
            'course': Course,
            'grade': Grade,
            'registration': Registration
        }

    return app

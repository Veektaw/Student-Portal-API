from ..utility import db
import random, string

class Student(db.Model):
    __tablename__  = 'students'

    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    student_password = db.Column(db.Text(), nullable=False)
    courses = db.relationship('Course', secondary='registrations')
    grade = db.relationship('Grade', backref='student')

    def __repr__(self):
        return f"<student {self.id}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

from ..utility import db


class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer(), primary_key=True)
    course_name = db.Column(db.String(50), nullable=False)
    course_unit = db.Column(db.Integer(), default=8)
    course_teacher = db.Column(db.String(30), nullable=False)
    courses = db.relationship('Student', secondary='registrations')
    grade = db.relationship('Grade', backref='course')
    


    def __repr__(self):
        return f"<course {self.id}>"
    
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

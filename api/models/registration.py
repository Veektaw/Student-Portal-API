from ..utility import db

class Registration(db.Model):
    __tablename__  = 'registrations'

    last_name = db.Column(db.String(50))
    course_name = db.Column(db.String(50))
    student_email = db.Column(db.String(120))
    student_id = db.Column(db.Integer(), db.ForeignKey('students.id'), primary_key=True)
    course_id = db.Column(db.Integer(), db.ForeignKey('courses.id'), primary_key=True)

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
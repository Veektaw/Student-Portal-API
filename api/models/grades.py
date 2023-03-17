from ..utility import db


class Grade(db.Model):
    __tablename__  = 'grades'

    
    id = db.Column(db.Integer(), primary_key=True)
    last_name = db.Column(db.String(50))
    student_email = db.Column(db.String(50), unique=False)
    course_name = db.Column(db.String(50), nullable=True)
    student_grade = db.Column(db.Integer(), nullable=False)
    course_unit = db.Column(db.Integer, nullable=False)
    student_id = db.Column(db.Integer(), db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer(), db.ForeignKey('courses.id'), nullable=False)

    def __repr__(self):
        return f"<grade {self.id}>"
    
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
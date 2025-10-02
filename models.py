from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Faculty(db.Model):
    __tablename__ = 'faculty'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_hod = db.Column(db.Boolean, default=False)  # New field for HOD status

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    enrollment_number = db.Column(db.String(20), unique=True, nullable=False)
    semester = db.Column(db.String(20), nullable=False)
    group = db.Column(db.String(10), nullable=False)
    major_subject = db.Column(db.String(50), nullable=False)
    minor_subject = db.Column(db.String(50), nullable=False)
    multi_subject = db.Column(db.String(50), nullable=False)
    photo = db.Column(db.LargeBinary)
    face_encoding = db.Column(db.PickleType)
    
    # New fields
    gender = db.Column(db.String(10), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    mobile_number = db.Column(db.String(15), nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Student {self.name} ({self.enrollment_number})>'

class Attendance(db.Model):
    __tablename__ = 'attendance'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    department = db.Column(db.String(50), nullable=False)
    faculty = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    student = db.relationship('Student', backref=db.backref('attendances', lazy=True))

    def __repr__(self):
        return f'<Attendance {self.student.name} on {self.date}>'

class Syllabus(db.Model):
    __tablename__ = 'syllabus'
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    units = db.Column(db.String(500), nullable=False)  # Store units as comma-separated string

    def __repr__(self):
        return f'<Syllabus {self.department} - {self.semester} - {self.subject}>'

class Timetable(db.Model):
    __tablename__ = 'timetable'
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.String(50), nullable=False)
    day = db.Column(db.String(20), nullable=False)  # Monday, Tuesday, etc.
    time_slot = db.Column(db.String(20), nullable=False)  # e.g., "09:00-10:00"
    subject = db.Column(db.String(100), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'), nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    faculty = db.relationship('Faculty', backref=db.backref('timetable_entries', lazy=True))

    def __repr__(self):
        return f'<Timetable {self.department} - {self.semester} - {self.day} - {self.time_slot}>'

class SubjectCompletion(db.Model):
    __tablename__ = 'subject_completion'
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('syllabus.id'), nullable=False)
    unit = db.Column(db.String(50), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'), nullable=False)
    completed_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    subject = db.relationship('Syllabus', backref=db.backref('completions', lazy=True))
    faculty = db.relationship('Faculty', backref=db.backref('subject_completions', lazy=True))

    def __repr__(self):
        return f'<SubjectCompletion {self.subject.subject} - {self.unit}>' 
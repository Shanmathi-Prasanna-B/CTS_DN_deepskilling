# TASK 1: 
# SQLAlchemy — Define Models and Connect

# 75) Import necessary classes from sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Numeric
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

Base = declarative_base()

# 77) Define the 5 ORM model classes
class Department(Base):
    __tablename__ = 'departments'
    
    department_id = Column(Integer, primary_key=True, autoincrement=True)
    department_name = Column(String(100), nullable=False)
    
    # 78) Relationships
    students = relationship('Student', back_populates='department')
    courses = relationship('Course', back_populates='department')


class Student(Base):
    __tablename__ = 'students'
    
    student_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    enrollment_year = Column(Integer, nullable=False)
    department_id = Column(Integer, ForeignKey('departments.department_id'))
    
    # 78) Relationships
    # Many-to-one relationship to Department
    department = relationship('Department', back_populates='students')
    # One-to-many relationship to Enrollments
    enrollments = relationship('Enrollment', back_populates='student')


class Course(Base):
    __tablename__ = 'courses'
    
    course_id = Column(Integer, primary_key=True, autoincrement=True)
    course_code = Column(String(10), unique=True, nullable=False)
    course_name = Column(String(100), nullable=False)
    credits = Column(Integer, nullable=False)
    department_id = Column(Integer, ForeignKey('departments.department_id'))
    
    # Relationships
    department = relationship('Department', back_populates='courses')
    enrollments = relationship('Enrollment', back_populates='course')


class Professor(Base):
    __tablename__ = 'professors'
    
    professor_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    department_id = Column(Integer, ForeignKey('departments.department_id'))


class Enrollment(Base):
    __tablename__ = 'enrollments'
    
    enrollment_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.student_id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.course_id'), nullable=False)
    enrollment_date = Column(Date, nullable=False)
    grade = Column(String(2))
    
    # 78) Relationships
    # Many-to-one relationships to both Student and Course
    student = relationship('Student', back_populates='enrollments')
    course = relationship('Course', back_populates='enrollments')



# 76) Define an engine connecting to your target database
# Format: mysql+pymysql://user:password@host:port/database_name
DATABASE_URL = "mysql+pymysql://root:enter_password@127.0.0.1:3306/college_db_orm"

try:
    engine = create_engine(DATABASE_URL, echo=True) 
    
    # 79) Auto-create tables in the database
    print("\nGenerating schema frameworks through SQLAlchemy ORM")
    Base.metadata.create_all(engine)
    print("Execution Complete. Check your SQL client\n")

except Exception as e:
    print(f"\n Error: {e}")
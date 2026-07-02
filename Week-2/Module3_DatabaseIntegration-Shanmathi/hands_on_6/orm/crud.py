# TASK 2: 
# CRUD Operations via ORM

import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Department, Student, Course, Enrollment

# 80) Establish engine and set sessionmaker configuration
DATABASE_URL = "mysql+pymysql://root:enter_password@127.0.0.1:3306/college_db_orm"
engine = create_engine(DATABASE_URL, echo=True)

Session = sessionmaker(bind=engine)
session = Session()

try:
    # 81) INSERT: Add 3 Department objects and 5 Student objects
    print("\n--- [INSERTING DEPARTMENTS & STUDENTS] ---")
    
    cs_dept = Department(department_name="Computer Science")
    ee_dept = Department(department_name="Electrical Engineering")
    math_dept = Department(department_name="Mathematics")
    
    session.add_all([cs_dept, ee_dept, math_dept])
    session.flush()

    s1 = Student(first_name="Alice", last_name="Smith", email="alice@example.com", enrollment_year=2022, department=cs_dept)
    s2 = Student(first_name="Bob", last_name="Jones", email="bob@example.com", enrollment_year=2022, department=cs_dept)
    s3 = Student(first_name="Charlie", last_name="Brown", email="charlie@example.com", enrollment_year=2023, department=ee_dept)
    s4 = Student(first_name="David", last_name="Miller", email="david@example.com", enrollment_year=2021, department=math_dept)
    s5 = Student(first_name="Eva", last_name="Davis", email="eva@example.com", enrollment_year=2023, department=cs_dept)

    session.add_all([s1, s2, s3, s4, s5])
    session.commit()

    # 82) INSERT: Add 3 Course objects and 4 Enrollment objects
    print("\n--- [INSERTING COURSES & ENROLLMENTS] ---")
    
    c1 = Course(course_code="CS101", course_name="Intro to Programming", credits=4, department=cs_dept)
    c2 = Course(course_code="CS102", course_name="Data Structures", credits=4, department=cs_dept)
    c3 = Course(course_code="MATH201", course_name="Calculus II", credits=3, department=math_dept)
    
    session.add_all([c1, c2, c3])
    session.flush()

    today = datetime.date.today()
    e1 = Enrollment(student=s1, course=c1, enrollment_date=today, grade="A")
    e2 = Enrollment(student=s2, course=c1, enrollment_date=today, grade="B")
    e3 = Enrollment(student=s5, course=c2, enrollment_date=today, grade=None)
    e4 = Enrollment(student=s4, course=c3, enrollment_date=today, grade="A")

    session.add_all([e1, e2, e3, e4])
    session.commit()

    # 83) READ: Query all students in department 'Computer Science'
    print("\n--- [READ: COMPUTER SCIENCE STUDENTS] ---")
    cs_students = (
        session.query(Student)
        .join(Department)
        .filter(Department.department_name == "Computer Science")
        .all()
    )
    for student in cs_students:
        print(f"CS Student Found: {student.first_name} {student.last_name}")

    # 84) READ: Query all enrollments (Demonstrating N+1) 
    # LAZY LOADING (the N+1 problem)
    # (Commented out after observation so it doesn't clutter the final run logs)
    print("\n--- [APPROACH 1: READ ALL ENROLLMENTS (LAZY LOADING - N+1)] ---")
    # enrollments_lazy = session.query(Enrollment).all()
    # for enroll in enrollments_lazy:
    #     print(f"Lazy Load: Student: {enroll.student.first_name} | Course: {enroll.course.course_name}")


    # 88. Rewrite the query using joinedload: 
    print("\n--- [APPROACH 2: READ ALL ENROLLMENTS (FIXED WITH joinedload)] ---")
    from sqlalchemy.orm import joinedload
    
    enrollments_eager = (
        session.query(Enrollment)
        .options(
            joinedload(Enrollment.student), 
            joinedload(Enrollment.course)
        )
        .all()
    )
    
    for enroll in enrollments_eager:
        print(f"Eager Load: Student: {enroll.student.first_name} {enroll.student.last_name} | Course: {enroll.course.course_name}")

    # 85) UPDATE: Find a specific student by email and update enrollment_year
    print("\n--- [UPDATE: STUDENT ENROLLMENT YEAR] ---")
    target_student = session.query(Student).filter(Student.email == "alice@example.com").first()
    if target_student:
        target_student.enrollment_year = 2024
        session.commit()
        print(f"Updated {target_student.first_name}'s enrollment year to {target_student.enrollment_year}")

    # 86) DELETE: Remove an enrollment record
    print("\n--- [DELETE: ENROLLMENT RECORD] ---")

    enrollment_to_delete = session.query(Enrollment).filter(Enrollment.enrollment_id == e4.enrollment_id).first()
    if enrollment_to_delete:
        session.delete(enrollment_to_delete)
        session.commit()
        
        check_exists = session.query(Enrollment).filter(Enrollment.enrollment_id == e4.enrollment_id).first()
        print(f"Verification Check: Does enrollment exist? {'Yes' if check_exists else 'No (Successfully Removed)'}")

except Exception as e:
    session.rollback()
    print(f"Transaction failed, changes rolled back safely. Error: {e}")
finally:
    session.close()


# =======================================================================
# EXPECTED OUTCOME & N+1 ANALYSIS PERFORMANCE OBSERVATIONS
# =======================================================================
#
# When watching the terminal output during step 84 (READ All Enrollments):
# 
# 1. SQLAlchemy first issues 1 massive query to pull all items from the enrollments table:
#    SELECT enrollments.enrollment_id ... FROM enrollments;
#
# 2. Then, as script loops through the 4 records, every time it encounters 
#    enroll.student or enroll.course, it realizes it doesn't have that data in memory yet.
#    It instantly freezes code execution, fires a separate single lookup query to the database, 
#    and repeats this step on every single item in the collection.
#
# TOTAL QUERIES ENCOUNTERED IN STEP 84: 9 separate SQL queries issued to fetch only 4 records
# This is an N+1 problem path in action.


"""
89) QUERY COMPARISON TABLE
-------------------------------------------------------------------------
| Metric                   | Approach 1: Lazy Loading   | Approach 2: Eager Loading   |
|--------------------------|----------------------------|----------------------------|
| Total SQL Queries Issued | 5 Queries                  | 1 Query                    |
| Database Roundtrips      | 1 Base + 4 Lazy Lookups    | 1 Unified Join Query       |
| SQL Join Strategy        | None (Independent Lookups) | LEFT OUTER JOIN            |
| Performance Risk         | High O(N) Network Overhead | Scalable O(1) Query Cost   |
-------------------------------------------------------------------------

90) DIFFERENCES IN THE LOGS

1. LAZY LOADING BEHAVIOR (Approach 1 Logs):
   SQLAlchemy initially paused after fetching the base enrollment records. As the 
   Python loop processed each record, it was forced to hit the database 
   step-by-step on demand to collect missing related properties:
   
   -> SELECT enrollments.enrollment_id ... FROM enrollments;
   -> SELECT courses.course_id ... WHERE courses.course_id = 1;
   -> SELECT courses.course_id ... WHERE courses.course_id = 2;
   -> SELECT students.student_id ... WHERE students.student_id = 4;
   -> SELECT courses.course_id ... WHERE courses.course_id = 3;

2. EAGER LOADING BEHAVIOR (Approach 2 Logs - The Fix):
   By appending '.options(joinedload(...))' to the pipeline, the ORM combined the 
   entire lookup up front using explicit database relational optimization joins. 
   This cleanly populated all attributes into application memory before execution 
   entered the print iteration loop:
   
   -> SELECT enrollments.enrollment_id, ..., students_1.student_id, ..., courses_1.course_id ...
      FROM enrollments 
      LEFT OUTER JOIN students AS students_1 ON students_1.student_id = enrollments.student_id 
      LEFT OUTER JOIN courses AS courses_1 ON courses_1.course_id = enrollments.course_id;

CONCLUSION:
Eager loading completely eliminated the N+1 problem path, reducing the total query 
count from 5 down to exactly 1 database trip.
"""
# =======================================================================
-- TASK 1 
-- Creation of Database and Tables

CREATE DATABASE college_db;
USE college_db;

-- creation of tables 

CREATE TABLE students(
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    date_of_birth DATE,
    department_id INT NOT NULL,
    enrollment_year INT
);

CREATE TABLE departments(
    department_id INT PRIMARY KEY AUTO_INCREMENT,
    dept_name VARCHAR(100) NOT NULL,
    hod_name VARCHAR(100),
    budget DECIMAL(12,2)
);

ALTER TABLE students
ADD CONSTRAINT fk_students_departments
FOREIGN KEY (department_id) REFERENCES departments(department_id);

CREATE TABLE courses (
    course_id INT PRIMARY KEY AUTO_INCREMENT,
    course_name VARCHAR(150) NOT NULL,
    course_code VARCHAR(20) UNIQUE NOT NULL,
    credits INT,
    department_id INT NOT NULL,
    CONSTRAINT fk_courses_departments 
        FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

CREATE TABLE professors (
    professor_id INT PRIMARY KEY AUTO_INCREMENT,
    prof_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    department_id INT NOT NULL,
    salary DECIMAL(10,2),
    CONSTRAINT fk_professors_departments 
        FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

CREATE TABLE enrollments (
    enrollment_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    enrollment_date DATE DEFAULT (CURRENT_DATE),
    grade CHAR(2) NULL, -- Nullable as grades are assigned after completion
    CONSTRAINT fk_enrollments_students 
        FOREIGN KEY (student_id) REFERENCES students(student_id),
    CONSTRAINT fk_enrollments_courses 
        FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

-- Task 2
-- Normalisation Verification

-- 1NF Compliance: Every column holds atomic values. There are no multi-valued 
--                 attributes like comma-separated lists of grades or dates.
-- 2NF Compliance: The table uses 'enrollment_id' as a surrogate primary key, 
--                 while (student_id, course_id) forms a composite candidate key. 
--                 The non-key attributes 'enrollment_date' and 'grade' depend 
--                 fully on the entire composite key. No partial dependencies exist.
-- 3NF Compliance: There are no transitive dependencies. Non-key attributes 
--                 ('enrollment_date', 'grade') depend solely on the primary identifier 
--                 and do not rely on or determine any other non-key attributes.
-- Note on 3NF:    If 'dept_name' were added to the 'students' table, it would 
--                 create a transitive dependency (student_id -> department_id -> dept_name), 
--                 which is correctly avoided here by using a separate 'departments' table.

-- Task 3
-- Altering and Extending the Schema

ALTER TABLE students ADD COLUMN phone_number VARCHAR(15);

ALTER TABLE courses ADD COLUMN max_seats INT DEFAULT 60;

ALTER TABLE enrollments ADD CONSTRAINT chk_grade CHECK (grade IN ('A', 'B', 'C', 'D', 'F'));

ALTER TABLE departments CHANGE COLUMN hod_name head_of_dept VARCHAR(100);

ALTER TABLE students DROP COLUMN phone_number;

-- Verifying
SELECT table_name, column_name, data_type, column_default 
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE table_schema = 'college_db' 
  AND (
    (table_name = 'courses' AND column_name = 'max_seats') OR 
    (table_name = 'departments' AND column_name = 'head_of_dept') OR
    (table_name = 'students' AND column_name = 'phone_number')
  );

-- renaming head_of_dept back to hod_name
alter table departments change column head_of_dept hod_name varchar(100);
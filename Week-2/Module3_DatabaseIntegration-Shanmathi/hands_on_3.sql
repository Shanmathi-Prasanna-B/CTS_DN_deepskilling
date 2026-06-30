-- TASK 1 
-- Sub queries 

USE college_db;

-- 35) Find all students enrolled in more courses than avg number of enrollments per student. 
SELECT CONCAT(s.first_name, ' ', s.last_name) AS name, COUNT(e.course_id) AS enrollment_count
FROM students s 
JOIN enrollments e ON e.student_id = s.student_id  
GROUP BY s.student_id, s.first_name, s.last_name
HAVING COUNT(e.course_id) > (
    SELECT AVG(course_count) 
    FROM (
        SELECT s_all.student_id, COUNT(e_all.course_id) AS course_count 
        FROM students s_all
        LEFT JOIN enrollments e_all ON s_all.student_id = e_all.student_id
        GROUP BY s_all.student_id
    ) AS complete_student_totals
);
-- 36) List courses in which all enrolled students have received a grade of 'A'.
SELECT c.course_name 
FROM courses c 
JOIN enrollments e ON c.course_id = e.course_id 
GROUP BY c.course_id, c.course_name HAVING COUNT(e.student_id)=
SUM(CASE WHEN e.grade='A' THEN 1 ELSE 0 END);

-- 37) Find the professor with the highest salary in each department using a correlated subquery.
SELECT p.prof_name, p.department_id, p.salary 
FROM professors p 
WHERE p.salary = (
    SELECT MAX(inner_p.salary) 
    FROM professors inner_p 
    WHERE inner_p.department_id = p.department_id
);

-- 38) Using a subquery in the FROM clause (derived table), calculate the per-department average salary
-- and then filter to departments where that average exceeds 85,000
SELECT department,average from
(select d.dept_name as department,AVG(p.salary) as average from departments d right join professors p on p.department_id=d.department_id 
GROUP BY d.dept_name,d.department_id) as avlist where average>85000;

-- TASK 2 
-- Creating and Using Views

-- 39) Create a view vw_student_enrollment_summary showing each student's full name, department,
-- number of courses enrolled in, and GPA (average grade converted: A=4, B=3, C=2, D=1, F=0).
CREATE VIEW vw_student_enrollment_summary as
SELECT concat(s.first_name,' ',s.last_name)
as full_name,d.dept_name as department,count(e.course_id) as no_of_courses,ROUND(avg(
    CASE e.grade
    WHEN 'A' THEN 4.0
    WHEN 'B' THEN 3.0
    WHEN 'C' THEN 2.0
    WHEN 'D' THEN 1.0
    WHEN 'F' THEN 0.0
    ELSE NULL
    END
),2) as gpa FROM
students s join departments d on s.department_id=d.department_id left join enrollments e on
s.student_id=e.student_id GROUP BY s.student_id, s.first_name, s.last_name, d.dept_name;

-- 40) Create a view vw_course_stats showing course_name, course_code, total_enrollments, and avg_gpa
-- for each course.
CREATE VIEW vw_course_stats as
SELECT c.course_name as course,c.course_code as course_code,
count(e.student_id) as total_enrollments,ROUND(avg(
    CASE e.grade
    WHEN 'A' THEN 4.0
    WHEN 'B' THEN 3.0
    WHEN 'C' THEN 2.0
    WHEN 'D' THEN 1.0
    WHEN 'F' THEN 0.0
    ELSE NULL
    END
),2) as gpa FROM
courses c left join enrollments e on
c.course_id=e.course_id GROUP BY c.course_id,c.course_code;

-- 41) Query vw_student_enrollment_summary to find students with GPA above 3.0.
select * from vw_student_enrollment_summary where gpa>3.0;

-- 42) Attempt to UPDATE a row through vw_student_enrollment_summary and note what happens.
-- Research and document in your comments why multi-table views are generally not updatable.
UPDATE vw_student_enrollment_summary 
SET gpa = 3.0 
WHERE full_name = 'Arjun Mehta';

-- ERROR RECEIVED:
-- ERROR 1288 (HY000): The target table vw_student_enrollment_summary of the UPDATE is not updatable

-- RESEARCH & DOCUMENTATION: Why multi-table views are generally not updatable
-- 
-- 1. AMBIGUITY AND INVERSE MAPPING: A view is a virtual window, not a physical table. 
--    When a view combines data from multiple tables (Students, Departments, Enrollments), 
--    the database engine cannot determine how an update should map back to the 
--    underlying base tables.
--
-- 2. PRESENCE OF AGGREGATIONS: Our summary view uses `COUNT()` and `AVG()`. 
--    Database management systems cannot backward-calculate an aggregated value.
--    Here i have cjhanged the gpa from 3.5 to 3.0 the database has no logical way
--    to know which specific class grade needs to be altered.

-- 3. ONE-TO-MANY RELATIONSHIPS: Modifying a column derived from a parent table 
--    (like `d.dept_name`) through a combined view would inadvertently alter that 
--    department's name for *every single student* assigned to it, rather than just 
--    the one student targeted by the row. MySQL strictly blocks this to protect data consistency.

-- 43) DROP both views and recreate vw_student_enrollment_summary as a view WITH CHECK OPTION
-- (use a single-table subset view for this step).
DROP VIEW vw_student_enrollment_summary;
DROP view vw_course_stats;
CREATE OR REPLACE VIEW vw_cs_students_subset AS
SELECT student_id, first_name, last_name, email, department_id, enrollment_year
FROM students
WHERE department_id = 1
WITH CHECK OPTION;

-- VERIFICATION OF CHECK OPTION
-- A. This operation will SUCCEED because department_id matches the view's WHERE filter (1)
INSERT INTO vw_cs_students_subset (first_name, last_name, email, department_id, enrollment_year)
VALUES ('Jane', 'Doe', 'jane.doe@college.edu', 1, 2026);

-- B. This operation will FAIL because department_id (2) violates the WITH CHECK OPTION filter
INSERT INTO vw_cs_students_subset (first_name, last_name, email, department_id, enrollment_year)
VALUES ('John', 'Smith', 'john.smith@college.edu', 2, 2026);

-- Task 3 
-- Stored Procedures and Transactions

-- 44) Write a stored procedure sp_enroll_student (MySQL) accepts student_id, course_id, 
-- and enrollment_date, checks for duplicate enrollment, and inserts the record.
DELIMITER $$
CREATE PROCEDURE sp_enroll_student(in stud_id INT,in c_id INT,in edate DATE)
BEGIN
     if exists(SELECT 1 from enrollments where student_id=stud_id and course_id=c_id)
     then signal SQLSTATE '45000'
          set MESSAGE_TEXT='Error: the record already exists';
     else
     insert into enrollments(student_id,course_id,enrollment_date) VALUES (stud_id,c_id,edate);
     END IF;
END$$
DELIMITER ; $$
call sp_enroll_student(1,5,'2026-06-26');
call sp_enroll_student(1,5,'2026-06-26');

-- 45) Write a procedure sp_transfer_student that moves a student from one department to another. 
-- Wrap the UPDATE and a log-insert into a new table department_transfer_log inside a single 
-- transaction. ROLLBACK if either statement fails.
CREATE table department_transfer_log(log_id INT PRIMARY KEY auto_increment,student_id int,
current_dept int,target_dept int,transfer_date date);
DELIMITER $$
CREATE PROCEDURE sp_transfer_student(in stud_id INT,in dep_id INT)
BEGIN
   if exists(select 1 from students where student_id=stud_id and department_id=dep_id)
    then
      signal SQLSTATE '45000'
      set MESSAGE_TEXT = 'student is already present in the target department';
   end if;
   BEGIN
   declare exit handler for sqlexception
     BEGIN
      rollback;
      resignal set MESSAGE_TEXT='transaction faced error. transaction rolled back';
    END;
    start transaction;
      set @current_dept_id = (select department_id from students where student_id=stud_id);
      update students set department_id=dep_id where student_id=stud_id;
      insert into department_transfer_log (student_id,current_dept,target_dept,transfer_date) 
      values(stud_id,@current_dept_id,dep_id,curdate());
    commit;
   END;
END$$
DELIMITER ; $$
call sp_transfer_student(1,2);
-- successfully transfer student from department 1 to 2
call sp_transfer_student(1,2);
-- displays error as the target department is same as the current department
-- if transaction fails ->ERROR 1644 (45000): transaction faced error. transaction rolled back

-- 46. Test the transaction by manually introducing an error (e.g., invalid foreign key) 
-- and verify that the first UPDATE is also rolled back.
-- lets try to transfer the student to department dept_id 8 which doesnt exist
call sp_transfer_student(1,8);
-- ERROR 1452 (23000): transaction faced error. transaction rolled back
-- hence the first update is also rolled back

-- 47. Use SAVEPOINT to create a mid-transaction checkpoint: insert two enrollment records; set a
-- SAVEPOINT after the first; deliberately fail the second; ROLLBACK TO SAVEPOINT and verify only
-- the first record was saved.
START TRANSACTION;
-- Action 1: Enroll student 1 into a valid course(Course 4)
CALL sp_enroll_student(1, 4, '2026-06-26');

-- Set our checkpoint right here
SAVEPOINT post_first_enrollment;

-- Action 2: attempt a duplicate enrollment (Course 4 again)
-- Expected Result: MySQL throws ERROR 1644 (45000): Error: the record already exists
CALL sp_enroll_student(1, 4, '2026-06-26');

-- Action 3: Since the duplicate step failed, roll back to our clean savepoint
ROLLBACK TO SAVEPOINT post_first_enrollment;

-- Action 4: Commit the remaining transaction
COMMIT;

-- Verification Check: 
-- Enrollment for course 4 successfully persisted,while the duplicate attempt was safely managed and cleaned up!
SELECT * FROM enrollments WHERE student_id = 1;
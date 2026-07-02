-- Task 1
-- Baseline Performance — No Indexes

-- 48) EXPLAIN FORMAT=JSON Execution Plan Output
/*
{
  "query_block": {
    "select_id": 1,
    "cost_info": {
      "query_cost": "6.04"
    },
    "nested_loop": [
      {
        "table": {
          "table_name": "s",
          "access_type": "ALL",
          "possible_keys": [
            "PRIMARY"
          ],
          "rows_examined_per_scan": 11,
          "rows_produced_per_join": 1,
          "filtered": "10.00",
          "cost_info": {
            "read_cost": "1.99",
            "eval_cost": "0.11",
            "prefix_cost": "2.10",
            "data_read_per_join": "906"
          },
          "used_columns": [
            "student_id",
            "first_name",
            "last_name",
            "enrollment_year"
          ],
          "attached_condition": "(`college_db`.`s`.`enrollment_year` = 2022)"
        }
      },
      {
        "table": {
          "table_name": "e",
          "access_type": "ref",
          "possible_keys": [
            "fk_enrollments_students",
            "fk_enrollments_courses"
          ],
          "key": "fk_enrollments_students",
          "used_key_parts": [
            "student_id"
          ],
          "key_length": "4",
          "ref": [
            "college_db.s.student_id"
          ],
          "rows_examined_per_scan": 1,
          "rows_produced_per_join": 1,
          "filtered": "100.00",
          "cost_info": {
            "read_cost": "1.83",
            "eval_cost": "0.18",
            "prefix_cost": "4.12",
            "data_read_per_join": "58"
          },
          "used_columns": [
            "student_id",
            "course_id"
          ]
        }
      },
      {
        "table": {
          "table_name": "c",
          "access_type": "ALL",
          "possible_keys": [
            "PRIMARY"
          ],
          "rows_examined_per_scan": 5,
          "rows_produced_per_join": 1,
          "filtered": "20.00",
          "using_join_buffer": "hash join",
          "cost_info": {
            "read_cost": "1.00",
            "eval_cost": "0.18",
            "prefix_cost": "6.04",
            "data_read_per_join": "1K"
          },
          "used_columns": [
            "course_id",
            "course_name"
          ],
          "attached_condition": "(`college_db`.`c`.`course_id` = `college_db`.`e`.`course_id`)"
        }
      }
    ]
  }
}
*/

-- 49) Scan Identification:
--     - Table `s` (students) shows an access_type of "ALL", indicating a Full Table Scan.
--     - Table `c` (courses) shows an access_type of "ALL", indicating a Full Table Scan 
--     - Table `e` (enrollments) avoids a full scan by utilizing the index "fk_enrollments_students".

-- 50) Baseline Performance Metrics:
--     - Total Estimated Query Cost: 6.04
--     - Rows Examined for `s` (students): 11 rows
--     - Rows Examined for `c` (courses): 5 rows per scan
--     - Rows Examined for `e` (enrollments): 1 row per scan


-- TASK 2
-- Add Indexes and Compare Plans

-- 51) Create a B-Tree index on students.enrollment_year
CREATE INDEX idx_students_enroll_year ON students(enrollment_year);

-- 52) Create a composite UNIQUE index on enrollments(student_id, course_id)
CREATE UNIQUE INDEX uq_student_course ON enrollments(student_id, course_id);

-- 53) Create an index on courses.course_code
CREATE INDEX idx_courses_code ON courses(course_code);

-- 55) Create an expression-based index to handle functional partial logic in MySQL
CREATE INDEX idx_partial_unevaluated_enrollments 
ON enrollments((CASE WHEN grade IS NULL THEN student_id END));

-- 54) Post-Index EXPLAIN FORMAT=JSON Execution Plan Analysis
/*
{
  "query_block": {
    "select_id": 1,
    "cost_info": {
      "query_cost": "8.00"
    },
    "nested_loop": [
      {
        "table": {
          "table_name": "s",
          "access_type": "ref",
          "possible_keys": [
            "PRIMARY",
            "idx_students_enroll_year"
          ],
          "key": "idx_students_enroll_year",
          "used_key_parts": [
            "enrollment_year"
          ],
          "key_length": "5",
          "ref": [
            "const"
          ],
          "rows_examined_per_scan": 6,
          "rows_produced_per_join": 6,
          "filtered": "100.00",
          "cost_info": {
            "read_cost": "0.50",
            "eval_cost": "0.60",
            "prefix_cost": "1.10",
            "data_read_per_join": "4K"
          },
          "used_columns": [
            "student_id",
            "first_name",
            "last_name",
            "enrollment_year"
          ]
        }
      },
      {
        "table": {
          "table_name": "e",
          "access_type": "ref",
          "possible_keys": [
            "uq_student_course",
            "fk_enrollments_courses"
          ],
          "key": "uq_student_course",
          "used_key_parts": [
            "student_id"
          ],
          "key_length": "4",
          "ref": [
            "college_db.s.student_id"
          ],
          "rows_examined_per_scan": 2,
          "rows_produced_per_join": 12,
          "filtered": "100.00",
          "using_index": true,
          "cost_info": {
            "read_cost": "1.50",
            "eval_cost": "1.20",
            "prefix_cost": "3.80",
            "data_read_per_join": "384"
          },
          "used_columns": [
            "student_id",
            "course_id"
          ]
        }
      },
      {
        "table": {
          "table_name": "c",
          "access_type": "eq_ref",
          "possible_keys": [
            "PRIMARY"
          ],
          "key": "PRIMARY",
          "used_key_parts": [
            "course_id"
          ],
          "key_length": "4",
          "ref": [
            "college_db.e.course_id"
          ],
          "rows_examined_per_scan": 1,
          "rows_produced_per_join": 12,
          "filtered": "100.00",
          "cost_info": {
            "read_cost": "3.00",
            "eval_cost": "1.20",
            "prefix_cost": "8.00",
            "data_read_per_join": "8K"
          },
          "used_columns": [
            "course_id",
            "course_name"
          ]
        }
      }
    ]
  }
}
*/

-- COMPARISON DOCUMENTATION (Baseline vs. New Optimized Plan):
--
-- 1. PLAN STRATEGY SHIFT (Full Table Scan -> Index Lookups):
--    - Table `s` (students): Successfully changed from "access_type": "ALL" to "access_type": "ref".
--      The engine uses the new B-Tree index `idx_students_enroll_year` instead of searching everything.
--    - Table `c` (courses): Upgraded from "ALL" (Full Scan) with an expensive memory Hash Join 
--      to a precise "access_type": "eq_ref". It loops instantly using the primary key structure.
--
-- 2. COVERING INDEX BENEFIT:
--    - Table `e` (enrollments): Shows `"using_index": true`. This means our composite index 
--      `uq_student_course` functions as a covering index for this query. MySQL reads the required data 
--      directly from the index tree without wasting time fetching the physical rows from disk.
--
-- 3. ELIMINATION OF THE HASH JOIN MEMORY POOL:
--    - Notice that `"using_join_buffer": "hash join"` has vanished entirely from table `c`. 
--      Since table `e` passes sorted index tracks down the chain, the database doesn't need to spend 
--      CPU cycles building and sizing arrays in system RAM cache.
-- The composite UNIQUE index prevents duplicate enrollment inserts.
-- ERROR 1553 (HY000): Cannot drop index 'uq_student_course': needed in a foreign key constraint

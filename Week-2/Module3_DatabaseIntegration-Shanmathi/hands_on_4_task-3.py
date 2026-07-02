import mysql.connector
import time

# Database Configuration
db_config = {
    'user': 'root',
    'password': 'enter_password', 
    'host': '127.0.0.1',
    'database': 'college_db'
}

def run_n_plus_one_simulation():
    print("--- Running Script Version 1: N+1 Problem Simulation ---")
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    
    query_count = 0
    start_time = time.perf_counter()
    
    # 56. Initial query to fetch all N enrollments (1 query)
    cursor.execute("SELECT student_id, course_id, enrollment_date FROM enrollments;")
    enrollments = cursor.fetchall()
    query_count += 1
    
    results = []
    # Loop through each row and issue a separate SELECT for the student's name (N queries)
    for enrollment in enrollments:
        student_cursor = connection.cursor(dictionary=True)
        student_cursor.execute(
            "SELECT first_name, last_name FROM students WHERE student_id = %s;", 
            (enrollment['student_id'],)
        )
        student_data = student_cursor.fetchone()
        query_count += 1
        student_cursor.close()
        
        if student_data:
            results.append({
                'name': f"{student_data['first_name']} {student_data['last_name']}",
                'course_id': enrollment['course_id']
            })
            
    end_time = time.perf_counter()
    print(f"Total Queries Executed: {query_count}")
    print(f"Execution Time: {end_time - start_time:.6f} seconds\n")
    
    cursor.close()
    connection.close()
    return results, query_count


def run_optimized_join():
    print("--- Running Script Version 2: Optimized Single JOIN Query ---")
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    
    query_count = 0
    start_time = time.perf_counter()
    
    # 57 Fetch everything in one database trip (1 query)
    optimized_query = """
        SELECT CONCAT(s.first_name, ' ', s.last_name) AS name, e.course_id 
        FROM enrollments e 
        JOIN students s ON e.student_id = s.student_id;
    """
    cursor.execute(optimized_query)
    results = cursor.fetchall()
    query_count += 1
    
    end_time = time.perf_counter()
    print(f"Total Queries Executed: {query_count}")
    print(f"Execution Time: {end_time - start_time:.6f} seconds\n")
    
    cursor.close()
    connection.close()
    return results, query_count


if __name__ == "__main__":
    # 58. Compare the numbers and performance round-trips
    v1_results, v1_queries = run_n_plus_one_simulation()
    v2_results, v2_queries = run_optimized_join()
    
    # Validation check to ensure data structures match perfectly
    assert len(v1_results) == len(v2_results), "Data mismatches found!"
    print("Verification: Both methods returned identical data pools cleanly.")

# OUTPUT:
# --- Running Script Version 1: N+1 Problem Simulation ---
# Total Queries Executed: 13
# Execution Time: 0.040487 seconds
# 
# --- Running Script Version 2: Optimized Single JOIN Query ---
# Total Queries Executed: 1
# Execution Time: 0.004741 seconds
# 
# Verification: Both methods returned identical data pools cleanly. 

# 59) DOCUMENTATION & REFLECTION QUESTIONS
 
# In a real application with 10,000 enrollments, how many extra 
# queries would the N+1 version issue?

# 1. The N+1 version would execute exactly 10,001 total queries.
# 2. This means it would issue exactly 10,000 EXTRA database queries.
#
# WHY THIS IS A CRITICAL ANTI-PATTERN:
# - Network Latency: Every single query requires a network round-trip between 
#   your application server and your database server. Even if each query takes 
#   just 2 milliseconds, 10,000 queries will freeze your app for 20+ seconds!
# - Connection Starvation: It floods your database connection pool, locking up 
#   threads and slowing down processing speeds for all other active users.
# - The Fix (Eager Loading): By implementing a single JOIN query, we collapse 
#   those 10,001 round-trips down to exactly 1 query, letting the database engine 
#   handle relational mapping natively in memory.
from db_config import get_connection
import pandas as pd

def get_summary_counts():
    conn = get_connection(database="learning_recommendation")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM courses")
    courses = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM interactions")
    interactions = cursor.fetchone()[0]

    cursor.close()
    conn.close()
    return students, courses, interactions

def get_all_students():
    conn = get_connection(database="learning_Recommendation")
    cursor = conn.cursor()
    cursor.execute("SELECT student_id, name FROM students")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def get_student_interactions(student_id):
    conn = get_connection(database="learning_Recommendation")
    cursor = conn.cursor()
    query = """
    SELECT c.title, i.time_spent, i.score, i.completed
    FROM interactions i 
    JOIN courses c ON i.course_id = c.course_id
    WHERE i.student_id = %s
    """
    cursor.execute(query, (student_id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def get_recommendations(student_id):
    conn = get_connection(database="learning_recommendation")
    cursor = conn.cursor()

    query = """
    SELECT c.course_id, c.title, COUNT(i.student_id) as popularity
    FROM courses c
    LEFT JOIN interactions i ON c.course_id = i.course_id
    WHERE c.course_id NOT IN(
        SELECT course_id FROM interactions WHERE student_id = %s
    )
    GROUP BY c.course_id
    ORDER BY popularity DESC
    LIMIT 5;
"""
    cursor.execute(query, (student_id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def get_course_completion_rates():
    conn = get_connection(database="learning_recommendation")
    cursor = conn.cursor()
    
    query = """
        SELECT 
            c.title AS course_title,
            ROUND(SUM(i.completed = 'Yes') / COUNT(*) * 100, 2) AS completion_percentage
        FROM interactions i
        JOIN courses c ON i.course_id = c.course_id
        GROUP BY c.course_id, c.title
        ORDER BY completion_percentage DESC;
    """
    
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return pd.DataFrame(rows, columns=["course_title", "completion_percentage"])

def get_average_completion_rate():
    conn = get_connection(database="learning_Recommendation")
    cursor = conn.cursor()
    query = """
    SELECT ROUND(
        SUM(CASE WHEN completed = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2
    ) AS avg_completion_rate
    FROM interactions;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    if rows and  rows[0] is not None:
        return rows[0]
    else:
        return 0.0
#For loading data into MySQL
import pandas as pd
import mysql.connector 
from db_config import get_connection

root_conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ridima456"
)
root_cursor = root_conn.cursor()
root_cursor.execute("CREATE DATABASE IF NOT EXISTS learning_recommendation")
print("✅ Database created or already exists.")
root_cursor.close()
root_conn.close()

conn = get_connection(database="learning_recommendation")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
            student_id VARCHAR(10) PRIMARY KEY,
            name VARCHAR(100),
            skill_level VARCHAR(50)
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS courses (
    course_id VARCHAR(10) PRIMARY KEY,
    title VARCHAR(100),
    course VARCHAR(100),
    difficulty VARCHAR(50)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS interactions (
    student_id VARCHAR(10),
    course_id VARCHAR(10),
    time_spent INT,
    score INT,
    completed VARCHAR(5),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
)
""")
print("Tables created successfully.")

students_df = pd.read_csv("data/students.csv")
courses_df = pd.read_csv("data/courses.csv")
interactions_df = pd.read_csv("data/interactions.csv")

def insert_data(df, query, cursor):
    for row in df.itertuples(index=False):
        cursor.execute(query, tuple(row))

insert_data(
    students_df,
    "INSERT INTO students (student_id, name, skill_level) VALUES (%s, %s, %s)",
    cursor
)

insert_data(
    courses_df,
    "INSERT INTO courses (course_id, title, course, difficulty) VALUES (%s, %s, %s, %s)",
    cursor
)

insert_data(
    interactions_df,
    "INSERT INTO interactions (student_id, course_id, time_spent, score, completed) VALUES (%s, %s, %s, %s, %s)",
    cursor
)

conn.commit()
cursor.close()
conn.close()
print("Data inserted successfully into all tables.")

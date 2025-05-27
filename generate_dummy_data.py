import pandas as pd
import random 
import os

os.makedirs("data", exist_ok=True)

student_ids = [f"s{100+i}" for i in range(35)]
names = [f"Student_{i}" for i in range(35)]
levels = [random.choice(["Beginner","Intermediate","Advanced"]) for _ in range(35)]

student_df = pd.DataFrame({
    "student_id":student_ids,
    "name":names,
    "level":levels
})
student_df.to_csv("data/students.csv", index=False)

courses = [
    ("C201", "Python Basics", "Programming", "Beginner"),
    ("C202", "Data Science 101", "Data Science", "Intermediate"),
    ("C203", "ML with Python", "AI", "Advanced"),
    ("C204", "SQL for Analysts", "Databases", "Intermediate"),
    ("C205", "Frontend Dev", "Web Development", "Beginner"),
    ("C206", "Statistics", "Math", "Intermediate"),
    ("C207", "Deep Learning", "AI", "Advanced"),
    ("C208", "Data Visualization", "Data Science", "Beginner"),
]

courses_df = pd.DataFrame(courses, columns=["course_id", "title", "subject", "difficulty"])
courses_df.to_csv("data/courses.csv", index=False)

interactions = []
for _ in range(50):  # simulate 50 course interactions
    sid = random.choice(student_ids)
    cid, *_ = random.choice(courses)
    time_spent = random.randint(10, 300)  # in minutes
    score = random.randint(40, 100)
    completed = "Yes" if score > 60 and time_spent > 60 else "No"
    interactions.append((sid, cid, time_spent, score, completed))

interactions_df = pd.DataFrame(interactions, columns=[
    "student_id", "course_id", "time_spent_minutes", "score", "completed"
])
interactions_df.to_csv("data/interactions.csv", index=False)

print("✅ Dummy data generated and saved in /data")
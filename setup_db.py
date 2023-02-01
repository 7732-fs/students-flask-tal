import sqlite3
import faker 
import random 

def execute_query(sql):
     with sqlite3.connect("students.db") as conn:
          cur=conn.cursor()
          cur.execute(sql)
          return cur.fetchall()

def create_tables():
     execute_query("""CREATE TABLE IF NOT EXISTS teachers (
          id INTEGER PRIMARY KEY,
          name TEXT NOT NULL,
          email TEXT NOT NULL UNIQUE 
     )
     """)
     execute_query("""CREATE TABLE IF NOT EXISTS courses (
          id INTEGER PRIMARY KEY,
          name TEXT NOT NULL,
          teacher TEXT NOT NULL,
          FOREIGN KEY (teacher) REFERENCES teachers (email)
     )
     """)
     execute_query("""CREATE TABLE IF NOT EXISTS students (
          id INTEGER PRIMARY KEY,
          name TEXT NOT NULL,
          email TEXT NOT NULL UNIQUE 
     )
     """)
     execute_query("""CREATE TABLE IF NOT EXISTS students_courses (
          id INTEGER PRIMARY KEY,
          student_id INTEGER, 
          course_id INTEGER UNIQUE,
          FOREIGN KEY (student_id) REFERENCES students (id),
          FOREIGN KEY (course_id) REFERENCES courses (id)
     )
     """)

def create_fake_data(student_num=20, course_num=5, teacher_num=3):
     fake=faker.Faker()
     for student in range(student_num):
          execute_query(f"INSERT INTO students (name, email) VALUES ('{fake.name()}', '{fake.email()}')")
     for teacher in range(teacher_num):
          execute_query(f"INSERT INTO teachers (name, email) VALUES ('{fake.name()}', '{fake.email()}')")
     courses=['python', 'java', 'html', 'css', 'javascript']
     for course_name in courses:
          teacher_emails=[ teacher[0] for teacher in execute_query("SELECT email from teachers") ]
          execute_query(f"INSERT INTO courses (name, teacher) VALUES ('{course_name}', '{random.choice(teacher_emails)}' )")
     

create_tables()
create_fake_data()

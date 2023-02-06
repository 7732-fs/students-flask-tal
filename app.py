from flask import Flask, request, url_for, render_template, redirect
from setup_db import execute_query
from sqlite3 import IntegrityError
from collections import namedtuple

app = Flask(__name__)

@app.route('/registrations/<student_id>')
def registrations(student_id):
     course_names=execute_query(f"""
     SELECT students.name, id FROM students WHERE students.id={student_id} UNION SELECT name, teacher from courses WHERE courses.id IN 
          (SELECT course_id FROM students_courses WHERE student_id={student_id})"""
     )
     course_objects=[namedtuple("Course", ["name", "teacher"])(*c) for c in course_names[1:]]
     student=course_names[0][0] # TODO: use namedtuple here also
     return render_template("registrations.html", student=student, courses=course_objects)

@app.route('/register/<student_id>/<course_id>')
def register(student_id, course_id):
     try:
          execute_query(f"INSERT INTO students_courses (student_id, course_id) VALUES ('{student_id}', '{course_id}')")
     except IntegrityError:
          return "student is already registered to this course"
     return redirect(url_for('registrations', student_id=student_id))

def test():
     print("done by tal-training")

if __name__ == '__main__':
    app.run(debug=True)
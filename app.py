from flask import Flask, request, url_for, render_template, redirect
from setup_db import execute_query
from sqlite3 import IntegrityError

app = Flask(__name__)

@app.route('/registrations/<student_id>')
def registrations(student_id):
     course_names=execute_query(f"""
     SELECT students.name FROM students WHERE students.id={student_id} UNION SELECT name from courses WHERE courses.id IN 
          (SELECT course_id FROM students_courses WHERE student_id={student_id})"""
     )
          # SELECT courses.name, courses.id from courses JOIN students_courses on students_courses.course_id=courses.id where students_courses.student_id=1
          #select students.name, id from students where id=1 UNION SELECT courses.name, courses.id from courses JOIN students_courses on students_courses.course_id=courses.id where students_courses.student_id=1
          #test
     return render_template("registrations.html", courses=course_names)

@app.route('/register/<student_id>/<course_id>')
def register(student_id, course_id):
     try:
          execute_query(f"INSERT INTO students_courses (student_id, course_id) VALUES ('{student_id}', '{course_id}')")
     except IntegrityError:
          return "student is already registered to this course"
     return redirect(url_for('registrations', student_id=student_id))

if __name__ == '__main__':
    app.run(debug=True)
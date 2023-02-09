from setup_db import create_tables, create_fake_data, execute_query

def test_db():
     create_tables()
     create_fake_data(student_num=20)
     num=execute_query("SELECT COUNT(id) FROM students")
     assert int(num[0][0])==20



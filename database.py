import mysql.connector

def get_connection():
    connection=mysql.connector.connect(
        host="localhost",
        user="root",
        password="@Yash192004",
        database="student_db",
        port=3306
    )
    return connection


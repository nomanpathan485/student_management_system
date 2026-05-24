from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


# CREATE TABLE

def create_table():

    connection = sqlite3.connect("student.db")

    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        marks INTEGER
    )
    """)

    connection.commit()

    connection.close()


create_table()


# HOME PAGE

@app.route("/")
def home():

    return render_template("index.html")


# ADD STUDENT

@app.route("/add", methods=["POST"])
def add_student():

    name = request.form["name"]

    marks = request.form["marks"]

    connection = sqlite3.connect("student.db")

    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO students (name, marks)
    VALUES (?, ?)
    """, (name, marks))

    connection.commit()

    connection.close()

    return redirect("/students")


# VIEW STUDENTS

@app.route("/students")
def students():

    connection = sqlite3.connect("student.db")

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM students")

    data = cursor.fetchall()

    connection.close()

    return render_template("students.html", students=data)


# DELETE STUDENT

@app.route("/delete/<int:id>")
def delete_student(id):

    connection = sqlite3.connect("student.db")

    cursor = connection.cursor()

    cursor.execute("""
    DELETE FROM students
    WHERE id = ?
    """, (id,))

    connection.commit()

    connection.close()

    return redirect("/students")


if __name__ == "__main__":
    app.run(debug=True)
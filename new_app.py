from flask import Flask, render_template, request, redirect
from database import get_connection

app = Flask(__name__)


# HOME PAGE + SEARCH
@app.route("/")
def home():

    search = request.args.get("search", "")

    con = get_connection()
    cursor = con.cursor(dictionary=True)

    query = """
        SELECT * FROM students
        WHERE name LIKE %s
        ORDER BY id DESC
    """

    cursor.execute(query, ("%" + search + "%",))

    students = cursor.fetchall()

    cursor.close()
    con.close()

    return render_template(
        "index.html",
        students=students,
        search=search
    )


# ADD STUDENT
@app.route("/add", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":

        name = request.form["name"]
        age = int(request.form["age"])
        course = request.form["course"]

        con = get_connection()
        cursor = con.cursor()

        query = """
            INSERT INTO students (name, age, course)
            VALUES (%s, %s, %s)
        """

        cursor.execute(query, (name, age, course))

        con.commit()

        cursor.close()
        con.close()

        return redirect("/")

    return render_template("add.html")


# DELETE STUDENT
@app.route("/delete/<int:id>", methods=["POST"])
def delete_student(id):

    con = get_connection()
    cursor = con.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id = %s",
        (id,)
    )

    con.commit()

    cursor.close()
    con.close()

    return redirect("/")


# EDIT STUDENT
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):

    con = get_connection()
    cursor = con.cursor(dictionary=True)

    if request.method == "POST":

        name = request.form["name"]
        age = int(request.form["age"])
        course = request.form["course"]

        query = """
            UPDATE students
            SET name = %s, age = %s, course = %s
            WHERE id = %s
        """

        cursor.execute(
            query,
            (name, age, course, id)
        )

        con.commit()

        cursor.close()
        con.close()

        return redirect("/")

    cursor.execute(
        "SELECT * FROM students WHERE id = %s",
        (id,)
    )

    student = cursor.fetchone()

    cursor.close()
    con.close()

    if student is None:
        return "Student Not Found", 404

    return render_template(
        "edit.html",
        student=student
    )


if __name__ == "__main__":
    app.run(debug=True)
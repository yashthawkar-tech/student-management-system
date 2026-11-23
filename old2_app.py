from flask import Flask, render_template, request, redirect

app = Flask(__name__)

students = [
    {"id": 1, "name": "Rahul", "age": 20, "course": "Python"},
    {"id": 2, "name": "Priya", "age": 21, "course": "Java"},
    {"id": 3, "name": "Amit", "age": 22, "course": "C++"}
]


# Home Page
@app.route("/")
def home():

    search = request.args.get("search", "")

    filtered_students = []

    for student in students:
        if search.lower() in student["name"].lower():
            filtered_students.append(student)

    return render_template(
        "index.html",
        students=filtered_students,
        search=search
    )


# Add Student
@app.route("/add", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":

        name = request.form["name"]
        age = int(request.form["age"])
        course = request.form["course"]

        new_student = {
            "id": max([s["id"] for s in students], default=0) + 1,
            "name": name,
            "age": age,
            "course": course
        }

        students.append(new_student)

        return redirect("/")

    return render_template("add.html")


# Delete Student
@app.route("/delete/<int:id>")
def delete_student(id):

    for student in students:
        if student["id"] == id:
            students.remove(student)
            break

    return redirect("/")


# Edit Student
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):

    student = None

    for s in students:
        if s["id"] == id:
            student = s
            break

    if student is None:
        return "Student Not Found", 404

    if request.method == "POST":

        student["name"] = request.form["name"]
        student["age"] = int(request.form["age"])
        student["course"] = request.form["course"]

        return redirect("/")

    return render_template("edit.html", student=student)


if __name__ == "__main__":
    app.run(debug=True)
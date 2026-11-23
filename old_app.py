from flask import Flask, render_template, request, redirect

app = Flask(__name__)

students = [
    {"id": 1, "name": "Rahul", "age": 20, "course": "Python"},
    {"id": 2, "name": "Priya", "age": 21, "course": "Java"}
]


@app.route("/")
def home():
    return render_template("index.html", students=students)


@app.route("/add", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        course = request.form["course"]

        new_student = {
            "id": len(students) + 1,
            "name": name,
            "age": age,
            "course": course
        }

        students.append(new_student)

        return redirect("/")

    return render_template("add.html")


@app.route("/delete/<int:id>")
def delete_student(id):

    for student in students:
        if student["id"] == id:
            students.remove(student)
            break

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
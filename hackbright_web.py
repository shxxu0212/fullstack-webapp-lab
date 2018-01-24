"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template, redirect, flash

import hackbright

app = Flask(__name__)
app.secret_key = 'omgsosecret'


@app.route("/student-add")
def student_add():
    """Add a new student landing page."""

    return render_template("create_student.html")

@app.route("/create-student", methods=['POST'])
def create_student():
    """Add a student."""

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    github = request.form.get('github')

    hackbright.make_new_student(first_name, last_name, github)
    flash("Thanks for adding {} {} with github {}".format(
        first_name, last_name, github))

    return redirect('/student?github={}'.format(github))


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")


@app.route("/")
def home_page():
    """Homepage"""

    names = hackbright.get_all_students()
    projects = hackbright.get_all_projects()

    return render_template("home.html", names=names, projects=projects)

@app.route("/grading")
def input_grades():
    """Grade Students, landing page"""

    names = hackbright.get_all_students()
    projects = hackbright.get_all_projects()

    return render_template("grading.html", names=names, projects=projects)

@app.route("/assign-grade", methods=["POST"])
def set_grades():
    """Add new grade to database"""

    github = request.form.get('student')
    title = request.form.get('project')
    grade = request.form.get('grade')

    grades = hackbright.get_grades_by_title(title)

    for grade in grades:
      if github in grade:
        hackbright.update_grade(github, title, grade)
      else:
        hackbright.assign_grade(github, title, grade)

    return redirect("/")

@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)
    grades = hackbright.get_grades_by_github(github)

    return render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github,
                           grades=grades)

    # return "{acct} is the GitHub account for {first} {last}".format(
    #     acct=github, first=first, last=last)

@app.route("/project-add")
def project_add():
    """Add a new project landing page."""

    return render_template("create_project.html")

@app.route("/create-project", methods=['POST'])
def create_project():
    """Add a project."""

    title = request.form.get('title')
    description = request.form.get('description')
    max_grade = request.form.get('max_grade')

    hackbright.make_new_project(title, description, max_grade)

    flash("Thanks for adding {}".format(title))

    return redirect('/project?title={}'.format(title))

@app.route("/project-search")
def get_project_info():
    """Show form for searching for a student."""

    return render_template("project_search.html")


@app.route("/project")
def get_project():
    """Show information about a student."""

    title = request.args.get('title')

    title, description, max_grade = hackbright.get_project_by_title(title)

    grades = hackbright.get_grades_by_title(title)

    return render_template("project_info.html",
                           title=title,
                           description=description,
                           max_grade=max_grade,
                           grades=grades)

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)

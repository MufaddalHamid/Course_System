import uuid

import requests
from Logic.TeacherBC import TeacherBC
from Logic.CourseBC import CourseBC
from Logic.LoginBC import LoginBC
from Logic.CategoryBC import CategoryBC

from Logic.AppHelper import roleType

# 7fbb8c8e6d9dccb5d6d614381b11a128020395d4
from flask import Flask, jsonify, render_template, request, redirect, url_for
import os
from Logic.AppHelper import ActiveSession

# test logic
from datetime import datetime, timedelta
from flask import make_response

app = Flask(__name__, template_folder='Views', static_url_path='/static/')

# region Index

@app.context_processor
def inject_role_type():
    return dict(roleType=roleType)


@app.route("/")
def home():
    return render_template('Forms/index.html')
# endregion

# region Login


@app.route("/Login", methods=['GET', 'POST'])
def Login():
    role = roleType()
    if (role == "student"):
        return render_template('Reports/StudentDashboard.html')
    elif (role == "faculty"):
        return render_template('Reports/TeacherDashboard.html')

    if (request.method == "POST"):
        email = request.form.get("email")
        password = request.form.get("password")
        rememberMe = request.form.get("remember")
        if (email == "test@faculty.com"):
            if (password == "test@faculty"):
                role = "faculty"
        elif (email == "test@student.com"):
            if (password == "test@student"):
                role = "student"
        else:
            return redirect(url_for(Login))
        response = make_response(redirect(url_for("Dashboard")))
        response.set_cookie('auth_token', role, expires=datetime.utcnow(
        ) + timedelta(days=2), secure=True, httponly=True, samesite='Strict')
        return response
    return render_template('Forms/Login.html')
# endregion

# region Dashboards


@app.route("/Dashboard")
def Dashboard():
    role = roleType()
    if (role == "student"):
        return render_template('Reports/StudentDashboard.html')
    elif (role == "faculty"):
        return render_template('Reports/TeacherDashboard.html')
    else:
        return redirect(url_for(Login))
# endregion

# region Teacher CRUD


@app.route("/Teacher")
def TeacherLising():
    # print(TeacherBC.get_books(self=None))
    role = roleType()
    if (role == "faculty"):
        return render_template('Listings/Teacher.html', teachers=TeacherBC(SysId=None).get_teachers())
    else:
        return redirect(url_for(Login))


@app.route('/Teacher/Create')
def CreateTeacher():
    # Add your logic for creating a book here

    role = roleType()
    if (role == "faculty"):
        return render_template('Forms/Teacher.html', teacher=TeacherBC(None), status='Create')
    else:
        return redirect(url_for(Login))


@app.route('/Teacher/Edit')
def EditTeacher():
    role = roleType()
    if (role == "faculty"):
        SysId = request.args.get('SysId')
        teacher = TeacherBC(SysId=SysId)
        return render_template('Forms/Teacher.html', teacher=teacher.get_teachers(), status='Edit')
    else:
        return redirect(url_for(Login))


@app.route('/SubmitTeacher', methods=['POST'])
def SubmitTeacher():
    if request.method == 'POST':
        role = roleType()
        if (role == "faculty"):
            if request.form.get('SysId') == 'None':
                teacher_bc = TeacherBC()
                return jsonify(teacher_bc.create_teacher(new_teacher=dict(request.form)))
            else:
                # print('Updating Valuesss',request.form.get('SysId'))
                teacher_bc = TeacherBC(SysId=request.form.get('SysId'))
                return jsonify(teacher_bc.update_teacher(new_data=dict(request.form)))
        else:
            return redirect(url_for(Login))


@app.route('/Teacher/Delete')
def DeleteTeacher():
    role = roleType()
    if (role == "faculty"):
        SysId = request.args.get('SysId')
        teacher = TeacherBC(SysId=SysId)
        return render_template('Forms/Teacher.html', teacher=teacher.get_teachers(), status='Delete')
    else:
        return redirect(url_for(Login))


@app.route('/Delete', methods=['POST'])
def Delete():
    if request.method == 'POST':
        role = roleType()
        if (role == "faculty"):
            if request.form.get('SysId') == 'None':
                return jsonify({"error": "No Teacher To Deelte"}, 500)
            else:
                teacher_bc = TeacherBC(SysId=request.form.get('SysId'))
                return jsonify(teacher_bc.delete_teacher())
        else:
            return redirect(url_for(Login))
# endregion

# region Course CRUD


@app.route("/Course")
def CourseLising():
    # print(TeacherBC.get_books(self=None))
    return render_template('Listings/Course.html', courses=CourseBC(SysId=None).get_courses())


@app.route('/Course/Create')
def CreateCourse():
    # Add your logic for creating a book here
    return render_template('Forms/Course.html', course=CourseBC(None), status='Create')


@app.route('/Course/Edit')
def EditCourse():
    SysId = request.args.get('SysId')
    course = CourseBC(SysId=SysId)
    return render_template('Forms/Course.html', course=course.get_courses(), status='Edit')


@app.route('/SubmitCourse', methods=['POST'])
def SubmitCourse():
    if request.method == 'POST':
        if request.form.get('SysId') == 'None':
            course_bc = CourseBC()
            return jsonify(course_bc.create_Course(new_course=dict(request.form)))
        else:
            # print('Updating Valuesss',request.form.get('SysId'))
            course_bc = CourseBC(SysId=request.form.get('SysId'))
            return jsonify(course_bc.update_Course(new_data=dict(request.form)))


@app.route('/Course/Delete')
def DeleteCourse():
    SysId = request.args.get('SysId')
    course = CourseBC(SysId=SysId)
    return render_template('Forms/Course.html', course=course.get_courses(), status='Delete')


@app.route('/DeleteC', methods=['POST'])
def DeleteC():
    if request.method == 'POST':
        if request.form.get('SysId') == 'None':
            return jsonify({"error": "No Course To Delete"}, 500)
        else:
            course_bc = CourseBC(SysId=request.form.get('SysId'))
            return jsonify(course_bc.delete_Course())
# endregion

# region Category CRUD


@app.route("/Categories")
def CategoryLising():
    # print(TeacherBC.get_books(self=None))
    return render_template('Listings/Category.html', categories=CategoryBC(SysId=None).get_categories())


@app.route('/Category/Create')
def CreateCategory():
    # Add your logic for creating a book here
    return render_template('Forms/Category.html', category=CategoryBC(None), status='Create')


@app.route('/Category/Edit')
def EditCategory():
    SysId = request.args.get('SysId')
    ctegory = CategoryBC(SysId=SysId)
    return render_template('Forms/Category.html', category=ctegory.get_categories(), status='Edit')


@app.route('/SubmitCategory', methods=['POST'])
def SubmitCategory():
    if request.method == 'POST':
        if request.form.get('SysId') == 'None':
            course_bc = CategoryBC()
            return jsonify(course_bc.create_Category(new_category=dict(request.form)))
        else:
            # print('Updating Valuesss',request.form.get('SysId'))
            course_bc = CategoryBC(SysId=request.form.get('SysId'))
            return jsonify(course_bc.update_Category(new_data=dict(request.form)))


@app.route('/Category/Delete')
def DeleteCategory():
    SysId = request.args.get('SysId')
    course = CategoryBC(SysId=SysId)
    return render_template('Forms/Category.html', category=course.get_categories(), status='Delete')


@app.route('/DeleteCa', methods=['POST'])
def DeleteCa():
    if request.method == 'POST':
        if request.form.get('SysId') == 'None':
            return jsonify({"error": "No Course To Delete"}, 500)
        else:
            course_bc = CategoryBC(SysId=request.form.get('SysId'))
            return jsonify(course_bc.delete_Category())
# endregion


if __name__ == "__main__":
    app.run(debug=True)

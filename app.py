import uuid

import requests
from Logic.TeacherBC import TeacherBC
from Logic.CourseBC import CourseBC
from Logic.CategoryBC import CategoryBC
from Logic.SubjectBC import SubjectBC
from Logic.StudentBC import StudentBC
# 7fbb8c8e6d9dccb5d6d614381b11a128020395d4
from flask import Flask, jsonify, render_template, request
import os
from Logic.AppHelper import ActiveSession

# test login imports
from flask import redirect, make_response, url_for
from Logic.AppHelper import roleType
from datetime import datetime, timedelta


app = Flask(__name__, template_folder='Views', static_url_path='/static/')

# region Index


@app.context_processor
def inject_role_type():
    return dict(roleType=roleType)


@app.route("/")
def home():
    # return render_template('Forms/index.html')
    return redirect(url_for("Login"))
# endregion

# region Login


@app.route("/Login", methods=['GET', 'POST'])
def Login():
    if (request.method == "POST"):
        email = request.form.get("email")
        password = request.form.get("password")
        rememberMe = request.form.get("remember")
        if (email == "test@faculty.com"):
            if (password == "test@faculty"):
                role = "teacher"
        elif (email == "test@student.com"):
            if (password == "test@student"):
                role = "student"
        else:
            return redirect(url_for("Login"))

        response = make_response(redirect(url_for("Dashboard")))
        response.set_cookie('auth_token', role, expires=datetime.utcnow(
        ) + timedelta(days=2), secure=True, httponly=True, samesite='Strict')
        return response
    role = roleType()
    if (role != None):
        return redirect(url_for("Dashboard"))
    return render_template('Forms/Login.html')
# endregion


# region Logout
@app.route('/Logout')
def Logout():
    role = roleType()
    if (role == None):
        return redirect(url_for("Login"))
    print("logout")
    resp = make_response(redirect(url_for("Login")))
    auth_token = None
    # resp.delete_cookie('auth_token', auth_token, secure=True, httponly=True, samesite='Strict')
    resp.delete_cookie('auth_token')
    # print("check" + resp)
    return resp

# endregion

# region Dashboards


@app.route("/Dashboard")
def Dashboard():
    # write logic to identify student or teacher
    role = roleType()
    if (role == "teacher"):
        return render_template('Reports/TeacherDashboard.html')
    elif (role == "student"):
        return render_template('Reports/StudentDashboard.html')
    else:
        return redirect(url_for("Login"))
    # return render_template('Reports/TeacherDashboard.html')
# endregion

# region Teacher CRUD


@app.route("/Teacher")
def TeacherLising():
    # print(TeacherBC.get_books(self=None))
    role = roleType()
    if (role == None):
        return redirect(url_for("Login"))

    return render_template('Listings/Teacher.html', teachers=TeacherBC(SysId=None).get_teachers())


@app.route('/Teacher/Create')
def CreateTeacher():
    # Add your logic for creating a book here
    role = roleType()
    if (role == "teacher"):
        return render_template('Forms/Teacher.html', teacher=TeacherBC(None), status='Create')

    return redirect(url_for("Login"))
    # return render_template('Forms/Teacher.html', teacher=TeacherBC(None), status='Create')


@app.route('/Teacher/Edit')
def EditTeacher():
    role = roleType()
    if (role == "teacher"):
        SysId = request.args.get('SysId')
        teacher = TeacherBC(SysId=SysId)
        return render_template('Forms/Teacher.html', teacher=teacher.get_teachers(), status='Edit')
    return redirect(url_for("Login"))


@app.route('/SubmitTeacher', methods=['POST'])
def SubmitTeacher():
    role = roleType()
    if (role == "teacher"):
        if request.method == 'POST':
            if request.form.get('SysId') == 'None':
                teacher_bc = TeacherBC()
                return jsonify(teacher_bc.create_teacher(new_teacher=dict(request.form)))
            else:
                # print('Updating Valuesss',request.form.get('SysId'))
                teacher_bc = TeacherBC(SysId=request.form.get('SysId'))
                return jsonify(teacher_bc.update_teacher(new_data=dict(request.form)))

    return jsonify({"Message": "Invalid Request"})


@app.route('/Teacher/Delete')
def DeleteTeacher():
    role = roleType()
    if (role == "teacher"):
        SysId = request.args.get('SysId')
        teacher = TeacherBC(SysId=SysId)
        return render_template('Forms/Teacher.html', teacher=teacher.get_teachers(), status='Delete')
    return redirect(url_for("Login"))


@app.route('/Delete', methods=['POST'])
def Delete():
    role = roleType()
    if (role == "Teacher"):
        if request.method == 'POST':
            if request.form.get('SysId') == 'None':
                return jsonify({"error": "No Teacher To Deelte"}, 500)
            else:
                teacher_bc = TeacherBC(SysId=request.form.get('SysId'))
                return jsonify(teacher_bc.delete_teacher())

    return jsonify({"Message": "Invalid Request"})
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

# region Subject CRUD


@app.route("/Subject")
def SubjectLising():
    # print(TeacherBC.get_books(self=None))
    print(SubjectBC(None).get_subjects())
    return render_template('Listings/Subject.html', subjects=SubjectBC(SysId=None).get_subjects())


@app.route('/Subject/Create')
def CreateSubject():
    # Add your logic for creating a book here
    return render_template('Forms/Subject.html', subject=SubjectBC(None), teachers=TeacherBC(SysId=None).get_teachers(), status='Create')


@app.route('/Subject/Edit')
def EditSubject():
    SysId = request.args.get('SysId')
    subject = SubjectBC(SysId=SysId)
    return render_template('Forms/Subject.html', subject=subject.get_subjects(), teachers=TeacherBC(SysId=None).get_teachers(), status='Edit')


@app.route('/SubmitSubject', methods=['POST'])
def SubmitSubject():
    if request.method == 'POST':
        if request.form.get('SysId') == 'None':
            subject_bc = SubjectBC()
            return jsonify(subject_bc.create_subject(new_subject=dict(request.form)))
        else:
            # print('Updating Valuesss',request.form.get('SysId'))
            subject_bc = SubjectBC(SysId=request.form.get('SysId'))
            return jsonify(subject_bc.update_subject(new_data=dict(request.form)))


@app.route('/Subject/Delete')
def DeleteSubject():
    SysId = request.args.get('SysId')
    subject = SubjectBC(SysId=SysId)
    return render_template('Forms/Subject.html', subject=subject.get_subjects(), teachers=TeacherBC(None).get_teachers(), status='Delete')


@app.route('/DeleteS', methods=['POST'])
def DeleteS():
    if request.method == 'POST':
        if request.form.get('SysId') == 'None':
            return jsonify({"error": "No Course To Delete"}, 500)
        else:
            course_bc = SubjectBC(SysId=request.form.get('SysId'))
            return jsonify(course_bc.delete_subject())

# endregion

# region Student CRUD


@app.route("/Student")
def StudentLising():
    # print(TeacherBC.get_books(self=None))
    print(StudentBC(None).get_students())
    return render_template('Listings/Student.html', students=StudentBC(SysId=None).get_students())


@app.route('/Student/Create')
def CreateStudent():
    # Add your logic for creating a book here
    return render_template('Forms/Student.html', student=StudentBC(None), courses=CourseBC(SysId=None).get_courses(), status='Create')


@app.route('/Student/Edit')
def EditStudent():
    SysId = request.args.get('SysId')
    student = StudentBC(SysId=SysId)
    return render_template('Forms/Student.html', student=student.get_students(), courses=CourseBC(SysId=None).get_courses(), status='Edit')


@app.route('/SubmitStudent', methods=['POST'])
def SubmitStudent():
    if request.method == 'POST':
        if request.form.get('SysId') == 'None':
            Student_bc = StudentBC()
            return jsonify(Student_bc.create_student(new_student=dict(request.form)))
        else:
            # print('Updating Valuesss',request.form.get('SysId'))
            Student_bc = StudentBC(SysId=request.form.get('SysId'))
            return jsonify(Student_bc.update_student(new_data=dict(request.form)))


@app.route('/Student/Delete')
def DeleteStudent():
    SysId = request.args.get('SysId')
    student = StudentBC(SysId=SysId)
    return render_template('Forms/Student.html', student=student.get_students(), courses=CourseBC(None).get_courses(), status='Delete')


@app.route('/DeleteSt', methods=['POST'])
def DeleteSt():
    if request.method == 'POST':
        if request.form.get('SysId') == 'None':
            return jsonify({"error": "No student To Delete"}, 500)
        else:
            course_bc = StudentBC(SysId=request.form.get('SysId'))
            return jsonify(course_bc.delete_student())
# endregion


if __name__ == "__main__":
    app.run(debug=True)

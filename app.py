import uuid
import requests
from Logic.TeacherBC import TeacherBC
from flask import Flask, jsonify, render_template, request
import os

import os
app = Flask(__name__, template_folder='Views', static_url_path='/static/')

# region Index
@app.route("/")
def home():
    if 'Login' == 'Student':
        pass
    return render_template('Forms/login.html')
# endregion

# region Login
@app.route("/Login")
def Login():
    return render_template('Forms/Login.html')
# endregion

#region Dashboards
@app.route("/Dashboard")
def Dashboard():
    # write logic to identify student or teacher
    #return render_template('Reports/StudentDashboard.html')
    return render_template('Reports/TeacherDashboard.html')
#endregion

#region Teacher CRUD
@app.route("/Teacher")
def TeacherLising():
    #print(TeacherBC.get_books(self=None))
    return render_template('Listings/Teacher.html', teachers = TeacherBC(SysId=None).get_teachers())
@app.route('/Teacher/Create')
def CreateTeacher():
    # Add your logic for creating a book here
    return render_template('Forms/Teacher.html', teacher = TeacherBC(None) , status = 'Create')
@app.route('/Teacher/Edit')
def EditTeacher():
    SysId = request.args.get('SysId')
    teacher = TeacherBC(SysId=SysId)
    return render_template('Forms/Teacher.html', teacher = teacher.get_teachers() , status = 'Edit')

@app.route('/SubmitTeacher', methods=['POST'])
def SubmitTeacher():
    if requests.method == 'POST':
        if request.form.get('SysId') == 'None':
            teacher_bc = TeacherBC()
            return jsonify(teacher_bc.create_teacher(new_teacher=dict(request.form)))
        else:
            #print('Updating Valuesss',request.form.get('SysId'))
            teacher_bc = TeacherBC(SysId=request.form.get('SysId'))
            return jsonify(teacher_bc.update_teacher(new_data=dict(request.form)))

@app.route('/Teacher/Delete')
def DeleteTeacher():
    SysId = request.args.get('SysId')
    teacher = TeacherBC(SysId=SysId)
    return render_template('Forms/Teacher.html', teacher=teacher.get_teacher() , status = 'Delete')

@app.route('/Delete', methods=['POST'])
def Delete():
    if request.method == 'POST':
        if request.form.get('SysId') == 'None':
            return jsonify({"error":"No Teacher To Deelte"},500)
        else:
            teacher_bc = TeacherBC(SysId=request.form.get('SysId'))
            return jsonify(teacher_bc.delete_teacher())
#endregion

if __name__ == "__main__":
    app.run(debug=True)
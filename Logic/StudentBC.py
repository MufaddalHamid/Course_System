import uuid
from datetime import date
from sqlalchemy import or_, and_
from Datamodel.Student import Student
from Logic.AppHelper import ActiveSession


class StudentBC:
    def __init__(self, SysId=None):
        self.SysId = SysId
        self.load_Student()

    def load_Student(self):
        try:
            if self.SysId is not None:
                print('SysID is not null')
                self.student = ActiveSession.Session.query(
                    Student).filter_by(SysId=self.SysId).first()
            else:
                print('SysId not provided, initialized empty Student')
                self.student = Student()
        except Exception as e:
            print(f"Error loading Student data: {str(e)}")
            self.student = None

    def create_student(self, new_student):
        try:
            self.student = Student(**new_student)
            student_exists = (
                ActiveSession.Session.query(Student)
                .filter(
                    or_(
                        Student.User_Name == self.student.User_Name,
                        Student.Email == self.student.Email,
                        Student.PRN == self.student.PRN
                    )
                )
                .first()
            )
            if student_exists:
                raise ValueError(
                    f'Student already exists!!')
            else:
                self.student.SysId = str(uuid.uuid4())
                ActiveSession.Session.add(self.student)
                ActiveSession.Session.commit()
                new_student['message'] = 'Student created successfully'
                new_student['SysId'] = str(self.student.SysId)
                new_student['Code'] = 201
                return new_student
        except Exception as e:
            ActiveSession.Session.rollback()
            new_student['message'] = str(e)
            new_student['Code'] = 500
            return new_student

    def get_students(self):
        try:
            if self.SysId is None:
                results = ActiveSession.Session.query(Student).all()
                return results
            else:
                if self.student:
                    return self.student
                else:
                    return {"error": "student not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 500

    def update_student(self, new_data):
        try:
            if self.student is not None:
                for key, value in new_data.items():
                    setattr(self.student, key, value)
                ActiveSession.Session.commit()
                return {"message": "student updated successfully ", "Code": 201}
            else:
                return {"message": "student not found", 'Code': 404}
        except Exception as e:
            ActiveSession.Session.rollback()
            return {"message": str(e), 'Code': 500}

    def delete_student(self):
        try:
            # Now you should be able to delete it
            ActiveSession.Session.delete(self.student)
            ActiveSession.Session.commit()
            return {"message": "Student deleted successfully", "Code": 201}
        except Exception as e:
            ActiveSession.Session.rollback()
            return {"message": str(e), "Code": 500}

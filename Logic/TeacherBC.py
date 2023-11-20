import uuid
from datetime import date
from sqlalchemy import or_, and_
from Datamodel.Teacher import Teacher
from Logic.AppHelper import ActiveSession


class TeacherBC:
    def __init__(self, SysId=None):
        self.SysId = SysId
        self.load_Teacher()

    def load_Teacher(self):
        try:
            if self.SysId is not None:
                print('SysID is not null')
                self.teacher = ActiveSession.Session.query(
                    Teacher).filter_by(SysId=self.SysId).first()
            else:
                print('SysId not provided, initialized emptyTeacher')
                self.teacher = Teacher()
        except Exception as e:
            print(f"Error loadingTeacher data: {str(e)}")
            self.teacher = None

    def create_teacher(self, new_teacher):
        try:
            self.teacher = Teacher(**new_teacher)
            teacher_exists = (
                ActiveSession.Session.query(Teacher)
                .filter(
                    or_(
                        Teacher.User_Name == self.teacher.User_Name,
                        Teacher.Email == self.teacher.Email
                    )
                )
                .first()
            )
            if teacher_exists:
                raise ValueError(
                    f'Teacher already existed | User already Created {teacher_exists.User_Name}!!')
            else:
                self.teacher.SysId = str(uuid.uuid4())
                ActiveSession.Session.add(self.teacher)
                ActiveSession.Session.commit()
                new_teacher['message'] = 'Teacher created successfully'
                new_teacher['SysId'] = str(self.teacher.SysId)
                new_teacher['Code'] = 201
                return new_teacher
        except Exception as e:
            ActiveSession.Session.rollback()
            new_teacher['message'] = str(e)
            new_teacher['Code'] = 500
            return new_teacher

    def get_teachers(self):
        try:
            if self.SysId is None:
                results = ActiveSession.Session.query(Teacher).all()
                return results
            else:
                if self.teacher:
                    return self.teacher
                else:
                    return {"error": "teacher not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 500

    def update_teacher(self, new_data):
        try:
            if self.teacher is not None:
                for key, value in new_data.items():
                    setattr(self.teacher, key, value)
                ActiveSession.Session.commit()
                return {"message": "teacher updated successfully ", "Code": 201}
            else:
                return {"message": "teacher not found", 'Code': 404}
        except Exception as e:
            ActiveSession.Session.rollback()
            return {"message": str(e), 'Code': 500}

    def delete_teacher(self):
        try:
            # Make sure self.teacher is loaded or associated with the active session
            if not ActiveSession.Session.object_session(self.teacher):
                print('went in function')
                # If it's not associated, query it from the database and add it to the session
                self.teacher = ActiveSession.Session.query(
                    Teacher).get(self.teacher.id)

            # Now you should be able to delete it
            ActiveSession.Session.delete(self.teacher)
            ActiveSession.Session.commit()
            return {"message": "Teacher deleted successfully", "Code": 201}
        except Exception as e:
            ActiveSession.Session.rollback()
            return {"message": str(e), "Code": 500}

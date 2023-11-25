import uuid
from datetime import date
from sqlalchemy import or_, and_
from Datamodel.Subject import Subject
from Logic.AppHelper import ActiveSession


class SubjectBC:
    def __init__(self, SysId=None):
        self.SysId = SysId
        self.load_Subject()

    def load_Subject(self):
        try:
            if self.SysId is not None:
                print('SysID is not null')
                self.subject = ActiveSession.Session.query(
                    Subject).filter_by(SysId=self.SysId).first()
            else:
                print('SysId not provided, initialized empty Subject')
                self.subject = Subject()
        except Exception as e:
            print(f"Error loading Subject data: {str(e)}")
            self.subject = None

    def create_subject(self, new_subject):
        try:
            self.subject = Subject(**new_subject)
            subject_exists = (
                ActiveSession.Session.query(Subject)
                .filter(
                    or_(
                        Subject.Subject_Name == self.subject.Subject_Name,
                        Subject.Teacher_ID == self.subject.Teacher_ID
                    )
                )
                .first()
            )
            if subject_exists:
                raise ValueError(
                    f'Subject already existed | Teacher already Used {subject_exists.Teacher.User_Name}!!')
            else:
                self.subject.SysId = str(uuid.uuid4())
                ActiveSession.Session.add(self.subject)
                ActiveSession.Session.commit()
                new_subject['message'] = 'Subject created successfully'
                new_subject['SysId'] = str(self.subject.SysId)
                new_subject['Code'] = 201
                return new_subject
        except Exception as e:
            ActiveSession.Session.rollback()
            new_subject['message'] = str(e)
            new_subject['Code'] = 500
            return new_subject

    def get_subjects(self):
        try:
            if self.SysId is None:
                results = ActiveSession.Session.query(Subject).all()
                return results
            else:
                if self.subject:
                    return self.subject
                else:
                    return {"error": "subject not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 500

    def update_subject(self, new_data):
        try:
            if self.subject is not None:
                for key, value in new_data.items():
                    setattr(self.subject, key, value)
                ActiveSession.Session.commit()
                return {"message": "subject updated successfully ", "Code": 201}
            else:
                return {"message": "subject not found", 'Code': 404}
        except Exception as e:
            ActiveSession.Session.rollback()
            return {"message": str(e), 'Code': 500}

    def delete_subject(self):
        try:
            # Now you should be able to delete it
            ActiveSession.Session.delete(self.subject)
            ActiveSession.Session.commit()
            return {"message": "Subject deleted successfully", "Code": 201}
        except Exception as e:
            ActiveSession.Session.rollback()
            return {"message": str(e), "Code": 500}

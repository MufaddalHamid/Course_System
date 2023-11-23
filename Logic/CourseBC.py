import uuid
from datetime import date
from sqlalchemy import or_, and_
from Datamodel.Course import Course
from Datamodel.Category import Category
from Datamodel.Category_Basket import Category_Basket
from Logic.AppHelper import ActiveSession


class CourseBC:
    def __init__(self, SysId=None):
        self.SysId = SysId
        self.load_Course()

    def load_Course(self):
        try:
            if self.SysId is not None:
                print('SysID is not null')
                self.course = ActiveSession.Session.query(
                    Course).filter_by(SysId=self.SysId).first()
            else:
                print('SysId not provided, initialized emptyCourse')
                self.course = Course()
        except Exception as e:
            print(f"Error loadingCourse data: {str(e)}")
            self.course = None

    def create_Course(self, new_course):
        try:
            print('Trying to create')
            self.course = Course(**new_course)
            course_exists = ActiveSession.Session.query(Course).filter_by(Course_Name=self.course.Course_Name).first()
            if course_exists:
                raise ValueError(
                    f'Course already existed | User already Created {course_exists.Course_Name}!!')
            else:
                self.course.SysId = str(uuid.uuid4())
                ActiveSession.Session.add(self.course)
                ActiveSession.Session.commit()
                new_course['message'] = 'Course created successfully'
                new_course['SysId'] = str(self.course.SysId)
                new_course['Code'] = 201
                return new_course
        except Exception as e:
            ActiveSession.Session.rollback()
            new_course['message'] = str(e)
            new_course['Code'] = 500
            return new_course

    def get_courses(self):
        try:
            if self.SysId is None:
                results = ActiveSession.Session.query(Course).all()
                return results
            else:
                if self.course:
                    return self.course
                else:
                    return {"error": "Course not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 500

    def update_Course(self, new_data):
        try:
            if self.course is not None:
                for key, value in new_data.items():
                    setattr(self.course, key, value)
                ActiveSession.Session.commit()
                return {"message": "Course updated successfully ", "Code": 201}
            else:
                return {"message": "Course not found", 'Code': 404}
        except Exception as e:
            ActiveSession.Session.rollback()
            return {"message": str(e), 'Code': 500}

    def delete_Course(self):
        try:
            # Make sure self.course is loaded or associated with the active session
            if not ActiveSession.Session.object_session(self.course):
                print('went in function')
                # If it's not associated, query it from the database and add it to the session
                self.course = ActiveSession.Session.query(
                    Course).get(self.course.id)

            # Now you should be able to delete it
            ActiveSession.Session.delete(self.course)
            ActiveSession.Session.commit()
            return {"message": "Course deleted successfully", "Code": 201}
        except Exception as e:
            ActiveSession.Session.rollback()
            return {"message": str(e), "Code": 500}

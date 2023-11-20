import uuid
from datetime import date
from sqlalchemy import or_, and_
from DataModel.Logins import Login
from Logic.AppHelper import ActiveSession


class LoginBC:
    def __init__(self, SysId=None):
        self.SysId = SysId
        self.load_Login()

    def load_Login(self):
        try:
            if self.SysId is not None:
                print('SysID is not null')
                self.login = ActiveSession.Session.query(
                    Login).filter_by(SysId=self.SysId).first()
            else:
                print('SysId not provided, initialized empty Login')
                self.teacher = Login()
        except Exception as e:
            print(f"Error loadingTeacher data: {str(e)}")
            self.login = None

    def registerUser(self, newUser):
        try:
            self.login = Login(**newUser)
            user_exists = (
                ActiveSession.Session.query(Login)
                .filter(
                    or_(Login.User_Name == self.login.User_Name)
                )
                .first()
            )
            if user_exists:
                raise ValueError(
                    f'User already existed | User already Created {user_exists.User_Name}!!')
            else:
                self.login.SysId = str(uuid.uuid4())
                ActiveSession.Session.add(self.login)
                ActiveSession.Session.commit()
                newUser['message'] = 'User created successfully'
                newUser['SysId'] = str(self.login.SysId)
                newUser['Code'] = 201
                return newUser
        except Exception as e:
            ActiveSession.Session.rollback()
            newUser['message'] = str(e)
            newUser['Code'] = 500
            return newUser

    def get_user(self, user):
        try:
            self.login = Login(**user)
            user_exists = ActiveSession.Session.query(Login).filter(
                Login.User_Name == self.login.User_Name
            ).first()
            if user_exists:
                return user_exists
            else:
                raise ValueError(f'User Does not Exist | User not Found')
        except Exception as e:
            return {"error": str(e)}, 500

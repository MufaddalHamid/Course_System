from sqlalchemy import Column, String, Enum
from Datamodel.BaseDM import BaseDM
from enum import Enum as PythonEnum

class UserType(PythonEnum):
    ADMIN = 0
    TEACHER = 1
    STUDENT = 2

class Login(BaseDM):
    __tablename__ = 'Logins'
    User_Name = Column(String(100), nullable=False)
    Password = Column(String(50), nullable=False)
    UserType = Column(Enum(UserType), nullable=False)  # Use Enum from enum module

# Rest of your code

from sqlalchemy import Column, BigInteger, String
from Datamodel.BaseDM import BaseDM
from enum import Enum
class UserType(Enum):
    ADMIN = 0
    TEACHER = 1
    STUDENT = 2

class Login_ID(BaseDM):
    tablename = 'Logins'
    User_Name = Column(String(100), nullable=False)
    Password = Column(String(50), nullable=False)
    UserType = Column(Enum( UserType , native_enum = False , nullable = False ))

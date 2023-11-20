from sqlalchemy import Column, BigInteger, String
from Datamodel.BaseDM import BaseDM
class Teacher(BaseDM):
    __tablename__ = 'Teacher'
    User_Name = Column(String(100), nullable=False)
    Password = Column(String(50), nullable=False)
    Email = Column(String(50), nullable=False)

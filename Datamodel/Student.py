from sqlalchemy import Column, BigInteger, String,Integer
from Datamodel.BaseDM import BaseDM
class Student(BaseDM):
    tablename = 'Student'
    User_Name = Column(String(100), nullable=False, unique=True)
    Password = Column(String(50), nullable=False)
    Email = Column(String(50), nullable=False, unique=True)
    Course_ID=Column(String(50), nullable=False)
    Year= Column(Integer, nullable=False)

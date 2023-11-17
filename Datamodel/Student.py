from sqlalchemy import Column, ForeignKey, String,Integer
from Datamodel.BaseDM import BaseDM
from Datamodel.Course import Course
from sqlalchemy.orm import relationship , backref
class Student(BaseDM):
    __tablename__ = 'Student'
    User_Name = Column(String(100), nullable=False, unique=True)
    Password = Column(String(50), nullable=False)
    Email = Column(String(50), nullable=False, unique=True)
    Course_ID = Column(String(36),ForeignKey(Course.SysId),nullable=False)
    Course = relationship(Course,backref = backref("Course"))
    Year = Column(Integer, nullable=False)

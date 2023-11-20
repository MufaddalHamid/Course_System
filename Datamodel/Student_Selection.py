from sqlalchemy import Column, ForeignKey, String,Integer
from sqlalchemy.orm import relationship , backref
from Datamodel.BaseDM import BaseDM
from Datamodel.Student import Student
from Datamodel.Category import Category
from Datamodel.Subject import Subject

class Student_Selection(BaseDM):
    __tablename__ = 'Student_Selection'
    Student_ID= Column(String(36),ForeignKey(Student.SysId),nullable=False)#Foreign Key
    Category_ID = Column(String(36),ForeignKey(Category.SysId),nullable=False)
    Subject_ID = Column(String(36),ForeignKey(Subject.SysId),nullable=False)
    Student = relationship(Student,backref=backref("Student_Selection"))
    Category = relationship(Category,backref=backref("Student_Selection"))
    Subject = relationship(Subject,backref=backref("Student_Selection"))

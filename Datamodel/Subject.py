from sqlalchemy import Column, ForeignKey, String,Integer
from Datamodel.BaseDM import BaseDM
from Datamodel.Teacher import Teacher
from Datamodel.Category import Category
from sqlalchemy.orm import relationship , backref
class Subject(BaseDM):
    __tablename__ = 'Subjects'
    Subject_Name = Column(String(100), nullable=False, unique=True)
    Teacher_ID= Column(String(36),ForeignKey(Teacher.SysId),nullable=True)
    PreRequisite_subject_id = Column(String(36), ForeignKey('Subjects.SysId'), nullable=True)
    Credit= Column(Integer, nullable=False)
    Teacher = relationship(Teacher,backref=backref("Subjects"))
    PreRequisite_subject = relationship('Subject', remote_side='Subject.SysId', backref=backref("Prerequisite_Subject"))
    # Category_ID = Column(String(36),ForeignKey(Category.SysId),nullable=False)
   # Category = relationship(Category ,backref=backref("Subjects"))
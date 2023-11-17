from sqlalchemy import Column, ForeignKey, String,Integer
from Datamodel.BaseDM import BaseDM
from Datamodel.Category import Category
from Datamodel.Subject import Subject
from sqlalchemy.orm import relationship , backref
class Subject_Basket(BaseDM):
    __tablename__ = 'Subject_Basket'
    Category_ID = Column(String(36),ForeignKey(Category.SysId),nullable=False)
    Subject_ID = Column(String(36), ForeignKey(Subject.SysId), nullable=False)
    Subject = relationship(Subject,backref=backref("Subject_Basket"))
    Category = relationship(Category, backref=backref("Category_Basket"))
    # Credit_per_Cat=Column(Integer(3),nullable=False)
    # Limit_per_Cat = Column(Integer(3),nullable=True)

from sqlalchemy import Column, ForeignKey, String,Integer
from Datamodel.BaseDM import BaseDM
from Datamodel.Category import Category
from Datamodel.Course import Course
from sqlalchemy.orm import relationship , backref
class Category_Basket(BaseDM):
    __tablename__ = 'Category_Basket'
    Category_ID= Column(String(36),ForeignKey(Category.SysId),nullable=False)
    Course_ID= Column(String(36),ForeignKey(Course.SysId),nullable=False)
    Credit_per_Cat=Column(Integer(),nullable=False)
    Limit_per_Cat = Column(Integer(),nullable=True)

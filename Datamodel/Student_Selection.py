from sqlalchemy import Column, BigInteger, String,Integer
from Datamodel.BaseDM import BaseDM
class Student_Selection(BaseDM):
    tablename = 'Student_Selection'
    Student_ID= Column(String(100), nullable=False,unique=True)#Foreign Key
    Subject_Select={(Category_ID):list(Subject_ID)}

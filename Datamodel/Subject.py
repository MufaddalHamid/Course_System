from sqlalchemy import Column, BigInteger, String,Integer
from Datamodel.BaseDM import BaseDM
class Subject(BaseDM):
    tablename = 'Subject_List'
    Subject_Name = Column(String(100), nullable=False, unique=True)
    Teacher_ID=Column(String(50), nullable=False)
    Category_ID = Column(String(50), nullable=False)
    Credit= Column(Integer, nullable=False)

from sqlalchemy import Column, BigInteger, String,Integer
from Datamodel.BaseDM import BaseDM
class Course(BaseDM):
    tablename = 'Course'
    Course_Name = Column(String(100), nullable=False, unique=True)
    Course_ID = Column(String(50), nullable=False)
    Duration = Column(Integer, nullable=False)
    Total_Credits = Column(Integer, nullable=False)
    Categories = list(Column(String(50), nullable=False)) #multivalued attribute

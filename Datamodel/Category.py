from sqlalchemy import Column, BigInteger, String,Integer
from Datamodel.BaseDM import BaseDM
class Category(BaseDM):
    __tablename__ = 'Category'
    Category_Name = Column(String(100), nullable=False, unique=True)
    #Subject_IDs = list( Column ( String (50) , nullable=False)) #multivalued attribute

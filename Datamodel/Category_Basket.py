from sqlalchemy import Column, BigInteger, String,Integer
from Datamodel.BaseDM import BaseDM
class Category_Basket(BaseDM):
    tablename = 'Category_Basket'
    Category_ID= Column(String(100), nullable=False)
    Course_ID= Column(String(100), nullable=False)
    Course_Category_ComboKey=[(Category_ID),(Course_ID)]
    Credit_per_Cat=Column(Integer(3),nullable=False)

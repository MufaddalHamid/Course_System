from sqlalchemy import Column, BigInteger, String,Integer
from Datamodel.BaseDM import BaseDM
class PreRequisite(BaseDM):
    tablename = 'Pre_Requisite'
    Subject_Name = Column(String(100), nullable=False, unique=True)
    PreRequisite_Sub_ID=Column(String(10), nullable=False)

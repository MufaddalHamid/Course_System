from sqlalchemy import Column, ForeignKey, String,Integer
from Datamodel.BaseDM import BaseDM
from Datamodel.Subject import Subject
class PreRequisite(BaseDM):
    tablename = 'Pre_Requisite'
    Subject_Name = Column(String(100), nullable=False, unique=True)
    Subject_Id = Column(String(36), ForeignKey(Subject.SysId), nullable=True)
    PreRequisite_Sub_ID=Column(String(36), ForeignKey(Subject.SysId), nullable=True)

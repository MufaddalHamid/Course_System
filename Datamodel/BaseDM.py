from sqlalchemy import Column, BigInteger, String
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()
class BaseDM(Base):
    __abstract__ = True
    SysId = Column(String(36), autoincrement=False,default=str(uuid.uuid4()), nullable=False, primary_key=True,)
    Srno = Column(BigInteger, autoincrement=True,server_default='1')
from sqlalchemy import Column, Integer, String, Float, Date

from DataModel.BaseDM import BaseDM



class AuthControl(BaseDM):
    __tablename__ = 'Auth_Access_Control'
    Auth_token = Column(String(100), nullable=False)
    role = Column(String(20), unique=True, nullable=False)
    expiry = Column(DateTime, default=datetime.utcnow() + timedelta(days=3), nullable=False)
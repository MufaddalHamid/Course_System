from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text, select

from Datamodel.BaseDM import Base
from DataModel import AuthControl

from flask import request
# endRegion

def delete_old_auth_Tokens(session):
    # PostgreSQL or MYSQL uses CURRENT_TIMESTAMP or NOW()
    session.execute(text('DELETE FROM "Auth_Access_Control" WHERE expiry < CURRENT_TIMESTAMP'))

    # SQLite uses CURRENT_TIMESTAMP or datetime('now')
    session.execute(text('DELETE FROM "Auth_Access_Control" WHERE expiry < CURRENT_TIMESTAMP'))
    session.commit()

def checkRole(session):

    cookies = request.cookies

    if ( 'auth_token' in cookies ):
        auth_token_value = cookies['auth_token']
        stmt = select(AuthControl).where(AuthControl.Auth_token == auth_token_value)
        result = session.execute(stmt)
        if(result.length > 1):
            return result.role
        else: 
            return False
        # session.query(AuthControl).all()
    

class ActiveSession:
    engine = create_engine('put your connection string!!')
    #this is my connection key put yours 'mssql+pyodbc://' + 'LAPTOP-LC07V53A/CourseSys?' + 'driver=SQL+Server+Native+Client+11.0'
    Session = sessionmaker(bind=engine)
    Session = Session()
    Base.metadata.create_all(engine)



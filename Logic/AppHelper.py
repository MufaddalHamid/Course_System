from Datamodel import AuthControl

from flask import request
from sqlalchemy import text, select


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
    

    else:
        return False
    

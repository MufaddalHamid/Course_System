from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text, select

from Datamodel.BaseDM import Base
from Datamodel.AuthControl import AuthControl

import secrets
from datetime import datetime, timedelta
from flask import request, make_response


def set_cookie():
    resp = make_response()
    auth_token = create_auth_token()
    resp.set_cookie('auth_token', auth_token, expires=datetime.utcnow() + timedelta(days=2))
    return resp


def remove_cookie():
    resp = make_response()
    resp.set_cookie('auth_token', '', expires=datetime.utcnow() - timedelta(days=-2))
    return resp


def create_auth_token(session, length=64):
    auth_token = secrets.token_hex(length)
    # todo 1: Add the auth_token to db
    # need session object again
    # insert it into db
    # todo 2: set role for auth token by fetching the respective role from db
    auth_control = AuthControl(Auth_token=auth_token, role="SET ROLE", expiry=(datetime.utcnow() + timedelta(days=2)))
    session.add(auth_control)
    return auth_token


def delete_old_auth_Tokens(session):
    # PostgreSQL or MYSQL uses CURRENT_TIMESTAMP or NOW()
    session.execute(text('DELETE FROM "Auth_Access_Control" WHERE expiry < CURRENT_TIMESTAMP'))

    # SQLite uses CURRENT_TIMESTAMP or datetime('now')
    session.execute(text('DELETE FROM "Auth_Access_Control" WHERE expiry < CURRENT_TIMESTAMP'))
    session.commit()


def checkRole(request, session):
    cookies = request.cookies
    if ('auth_token' in cookies):
        auth_token_value = cookies['auth_token']
        stmt = select(AuthControl).where(AuthControl.Auth_token == auth_token_value)
        result = session.execute(stmt)
        if (result.length > 1):
            return result.role
        else:
            return False
        # session.query(AuthControl).all()
    else:
        return False


class ActiveSession:
    engine = create_engine('put your connection string!!')
    # this is my connection key put yours 'mssql+pyodbc://' + 'LAPTOP-LC07V53A/CourseSys?' + 'driver=SQL+Server+Native+Client+11.0'
    Session = sessionmaker(bind=engine)
    Session = Session()
    Base.metadata.create_all(engine)


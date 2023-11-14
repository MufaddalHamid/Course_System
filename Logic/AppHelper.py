from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
# region DataModels
from Datamodel.BaseDM import Base
# endRegion

class ActiveSession:
    engine = create_engine('put your connection string!!')
    #this is my connection key put yours 'mssql+pyodbc://' + 'LAPTOP-LC07V53A/CourseSys?' + 'driver=SQL+Server+Native+Client+11.0'
    Session = sessionmaker(bind=engine)
    Session = Session()
    Base.metadata.create_all(engine)



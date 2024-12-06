from sqlmodel import create_engine, Session, SQLModel
from . import config

SQL_URL = config.setting.POSTGRES_URL

engine = create_engine(SQL_URL)

def get_db():
    try:
        session = Session(engine)
        print(f"Session created: {session}")  # Debugging
        yield session
    finally:
        print("Session closed")  # Debugging
        session.close()
        
def create_table():
    SQLModel.metadata.create_all(engine)
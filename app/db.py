from sqlmodel import create_engine, Session

SQL_URL = 'postgresql://postgres.thcwwywdjkztbvpcjehu:[YOUR-PASSWORD]@aws-0-ap-south-1.pooler.supabase.com:6543/postgres'

engine = create_engine(SQL_URL)

def get_db():
    with Session(engine) as session:
        yield session
        

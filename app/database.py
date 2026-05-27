from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_DATABASE_URL = ""
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


engine = create_engine(SQLALCHEMY_DATABASE_URL)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#     try:
#         conn = psycopg2.connect(
#             host="localhost", database="fastapi", 
#             user="postgres", password="<password>",
#             cursor_factory=RealDictCursor
#             )
#         cursur = conn.cursor()
#         print("databse connection was success")
#         break
#     except Exception as e:
#         time.sleep(2) 
#         print(e)
        # print("connection databse failed") bgtbbg
